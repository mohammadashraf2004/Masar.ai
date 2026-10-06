"""M06.L01 — RAG and Agents.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Source: Chapter 6, "RAG and Agents".
Instructor-authored curriculum adaptation based only on the supplied chapter.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M06.L01"

MODULE_ORDER = 6

MODULE_TITLE = "RAG and Agents"

MODULE_DESCRIPTION = (
    "Learn how to construct query-specific context with retrieval-augmented "
    "generation, optimize retrieval, build tool-using agents, design planning "
    "and reflection loops, evaluate agent failures, and manage short- and "
    "long-term memory."
)

SOURCE_CHAPTER = 6

SOURCE_PAGES = "Page range not provided in the supplied chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "RAG and Agents",

    "slug": "ai-engineering-m06-l01-rag-and-agents",

    "description": (
        "A complete learner-facing guide to retrieval-augmented generation and "
        "agentic AI: retrieval algorithms, vector search, hybrid search, chunking, "
        "reranking, query rewriting, multimodal and tabular RAG, tool use, "
        "planning, function calling, reflection, agent evaluation, and memory."
    ),

    "order": 1,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 5.5,

    "skill_tags": [
        "rag",
        "retrieval",
        "bm25",
        "tf-idf",
        "embeddings",
        "vector-search",
        "hybrid-search",
        "reranking",
        "chunking",
        "query-rewriting",
        "contextual-retrieval",
        "agents",
        "tool-use",
        "function-calling",
        "planning",
        "reflection",
        "agent-evaluation",
        "memory",
    ],

    "prerequisite_ids": [],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "RAG and Agents",

        "content": (
            "# RAG and Agents\n"
            "\n"
            "> **Course:** AI Engineering Foundations  \n"
            "> **Lesson:** M06.L01  \n"
            "> **Module:** RAG and Agents  \n"
            "> **Source alignment:** Chapter 6, *RAG and Agents*. This lesson is "
            "an instructor-authored curriculum adaptation rather than a "
            "reproduction of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why query-specific context improves foundation-model applications.\n"
            "- Describe the retrieve-then-generate pattern behind RAG.\n"
            "- Explain indexing and querying in a retriever.\n"
            "- Compare term-based and embedding-based retrieval.\n"
            "- Explain TF, IDF, TF-IDF, inverted indexes, and BM25 at a practical level.\n"
            "- Explain semantic retrieval, vector databases, k-NN, and approximate "
            "nearest-neighbor search.\n"
            "- Recognize common ANN approaches including LSH, HNSW, product "
            "quantization, IVF, and Annoy.\n"
            "- Evaluate retrievers using precision, recall, ranking metrics, latency, "
            "cost, build time, and index size.\n"
            "- Combine retrieval systems using reranking, hybrid search, and "
            "reciprocal rank fusion.\n"
            "- Design chunking, reranking, query rewriting, and contextual retrieval strategies.\n"
            "- Explain multimodal RAG and tabular RAG/text-to-SQL workflows.\n"
            "- Define an agent in terms of environment, actions, tools, and planning.\n"
            "- Distinguish knowledge-augmentation, capability-extension, and write tools.\n"
            "- Explain why multi-step agents compound errors and require stronger controls.\n"
            "- Separate planning from execution and include validation, reflection, "
            "and human approval where appropriate.\n"
            "- Explain function calling, planning granularity, hierarchical planning, "
            "and control-flow patterns.\n"
            "- Explain ReAct-style interleaving of reasoning, action, and observation.\n"
            "- Evaluate tool selection with ablation studies and tool-use analysis.\n"
            "- Identify agent planning, tool, goal, reflection, and efficiency failures.\n"
            "- Distinguish internal, short-term, and long-term memory.\n"
            "- Design memory-management strategies for long-running AI applications.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Context construction: the problem RAG and agents solve\n"
            "\n"
            "A model needs two things to solve a task well:\n"
            "\n"
            "1. **Instructions** — what it should do.\n"
            "2. **Information** — the facts, records, documents, or observations "
            "needed for this specific query.\n"
            "\n"
            "Instructions are often shared across many queries. Context is usually "
            "query-specific.\n"
            "\n"
            "If the model lacks the information needed for a question, it becomes "
            "more likely to guess, make mistakes, or hallucinate. This motivates "
            "two major context-construction patterns:\n"
            "\n"
            "- **RAG:** retrieve relevant information from external memory.\n"
            "- **Agents:** use tools to gather information or act in an environment.\n"
            "\n"
            "RAG is primarily a context-construction technique. Agents are broader: "
            "they can retrieve information, execute code, call APIs, write data, "
            "and perform multi-step tasks.\n"
            "\n"
            "A useful analogy is:\n"
            "\n"
            "```text\n"
            "Classical ML:     feature engineering gives the model useful inputs\n"
            "Foundation model: context construction gives the model useful information\n"
            "```\n"
            "\n"
            "[[IMAGE_NEEDED: Instructions versus query-specific context | A diagram "
            "showing a shared system instruction combined with query-specific "
            "retrieved/tool-generated context before entering the model | Learner "
            "should notice that instructions stay relatively stable while context "
            "changes for each query]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. RAG: retrieve first, then generate\n"
            "\n"
            "**Retrieval-augmented generation (RAG)** enhances generation by first "
            "retrieving relevant information from external memory sources.\n"
            "\n"
            "An external memory source can be:\n"
            "\n"
            "- An internal document database.\n"
            "- Previous conversations.\n"
            "- Product or customer data.\n"
            "- The internet.\n"
            "- Any external store the application can query.\n"
            "\n"
            "The basic pattern is:\n"
            "\n"
            "```text\n"
            "User query\n"
            "   -> retrieve relevant information\n"
            "   -> combine query + retrieved context\n"
            "   -> generative model\n"
            "   -> answer\n"
            "```\n"
            "\n"
            "RAG is useful when all potentially relevant knowledge cannot or should "
            "not be placed into every prompt.\n"
            "\n"
            "### Why long context does not automatically eliminate RAG\n"
            "\n"
            "Even if context windows become very large:\n"
            "\n"
            "- Application data can grow even faster.\n"
            "- Longer inputs cost more to process.\n"
            "- Longer inputs can add latency.\n"
            "- Models may fail to use every part of a long context effectively.\n"
            "- Extra irrelevant information can distract the model.\n"
            "\n"
            "Retrieval lets you spend context on the information most relevant to "
            "the current query.\n"
            "\n"
            "[[IMAGE_NEEDED: Basic RAG architecture | A simple pipeline showing "
            "query -> retriever -> external memory -> retrieved chunks -> prompt "
            "construction -> generator -> answer | Learner should notice the two "
            "core components: retriever and generator]]\n"
            "\n"
            "---\n"
            "\n"

            "## 3. RAG architecture: indexing and querying\n"
            "\n"
            "A basic RAG system contains:\n"
            "\n"
            "- A **retriever**, which finds relevant information.\n"
            "- A **generator**, which uses that information to produce an answer.\n"
            "\n"
            "The retriever itself has two major jobs.\n"
            "\n"
            "### Indexing\n"
            "\n"
            "Prepare external data so it can be retrieved quickly later.\n"
            "\n"
            "For document RAG, this may include:\n"
            "\n"
            "- Parsing documents.\n"
            "- Splitting documents into chunks.\n"
            "- Extracting terms or metadata.\n"
            "- Generating embeddings.\n"
            "- Building search indexes.\n"
            "\n"
            "### Querying\n"
            "\n"
            "Given a user's query, rank stored information by relevance and retrieve "
            "the best candidates.\n"
            "\n"
            "The success of the whole RAG system depends heavily on retrieval "
            "quality. A perfect generator cannot use information that the retriever "
            "never found.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. Term-based retrieval\n"
            "\n"
            "The simplest retrieval family scores documents using the words or "
            "terms they share with a query. This is also called **lexical retrieval**.\n"
            "\n"
            "### Term frequency (TF)\n"
            "\n"
            "If a query term appears many times in a document, the document may be "
            "more relevant to that term.\n"
            "\n"
            "```text\n"
            "TF(term, document) = number of times the term appears in the document\n"
            "```\n"
            "\n"
            "### Inverse document frequency (IDF)\n"
            "\n"
            "Some words appear everywhere and tell us little. Rare terms are often "
            "more informative.\n"
            "\n"
            "The chapter introduces the intuition:\n"
            "\n"
            "```text\n"
            "IDF(term) = total number of documents / number of documents containing term\n"
            "```\n"
            "\n"
            "Higher IDF means the term is rarer and therefore potentially more informative.\n"
            "\n"
            "### TF-IDF\n"
            "\n"
            "TF-IDF combines local importance inside a document with global rarity "
            "across the collection.\n"
            "\n"
            "A document receives a high score when important query terms occur often "
            "in that document but are relatively rare across the corpus.\n"
            "\n"
            "### Inverted index\n"
            "\n"
            "An inverted index maps terms to the documents that contain them.\n"
            "\n"
            "```text\n"
            "\"machine\" -> doc 1, doc 10, doc 38, doc 42\n"
            "\"banana\"  -> doc 5, doc 10\n"
            "```\n"
            "\n"
            "This makes keyword retrieval fast.\n"
            "\n"
            "### BM25\n"
            "\n"
            "BM25 is a widely used ranking algorithm derived from the same general "
            "ideas as TF-IDF. One important improvement is normalization for document "
            "length, because longer documents naturally contain more term occurrences.\n"
            "\n"
            "BM25 remains a strong practical baseline even when modern semantic "
            "retrieval is available.\n"
            "\n"
            "[[IMAGE_NEEDED: TF-IDF and inverted index intuition | A small corpus "
            "with an inverted index mapping rare and common query terms to documents, "
            "plus relevance scores | Learner should notice that frequent terms inside "
            "one document help, but terms common across every document carry less weight]]\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Tokenization matters for lexical search\n"
            "\n"
            "Term-based retrieval requires deciding what counts as a term.\n"
            "\n"
            "A naive tokenizer may split text by spaces, but that can destroy "
            "multi-word meaning. For example:\n"
            "\n"
            "```text\n"
            "\"hot dog\" -> \"hot\" + \"dog\"\n"
            "```\n"
            "\n"
            "Neither individual word means the same thing as the phrase.\n"
            "\n"
            "Possible preprocessing includes:\n"
            "\n"
            "- Lowercasing.\n"
            "- Removing punctuation.\n"
            "- Removing stop words.\n"
            "- Treating common n-grams as single terms.\n"
            "\n"
            "N-gram overlap can also support retrieval, although it is less "
            "discriminative when documents are much longer than queries.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Embedding-based retrieval\n"
            "\n"
            "Term matching looks at surface words. **Embedding-based retrieval** "
            "tries to match meaning.\n"
            "\n"
            "This is also called **semantic retrieval**.\n"
            "\n"
            "During indexing:\n"
            "\n"
            "```text\n"
            "document chunk -> embedding model -> vector -> vector database\n"
            "```\n"
            "\n"
            "During querying:\n"
            "\n"
            "```text\n"
            "query -> same embedding model -> query vector\n"
            "      -> find nearest document vectors\n"
            "      -> retrieve top-k chunks\n"
            "```\n"
            "\n"
            "The embedding model is critical. If it fails to place semantically "
            "related content near each other, retrieval will fail even if the "
            "vector database works perfectly.\n"
            "\n"
            "[[IMAGE_NEEDED: Semantic retrieval pipeline | A diagram showing "
            "documents embedded and stored in a vector database, then a query "
            "embedded by the same model and matched to nearby vectors | Learner "
            "should notice that indexing and querying must use compatible embeddings]]\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Vector databases and nearest-neighbor search\n"
            "\n"
            "A vector database must do more than store vectors. Its difficult job "
            "is finding vectors close to a query vector quickly.\n"
            "\n"
            "### Exact k-nearest neighbors (k-NN)\n"
            "\n"
            "A naive exact search can:\n"
            "\n"
            "1. Compare the query embedding with every stored vector.\n"
            "2. Rank all vectors by similarity.\n"
            "3. Return the top `k`.\n"
            "\n"
            "This is precise but expensive for large datasets.\n"
            "\n"
            "### Approximate nearest neighbors (ANN)\n"
            "\n"
            "Large vector stores usually trade a small amount of exactness for much "
            "faster search.\n"
            "\n"
            "The chapter introduces several important ANN families:\n"
            "\n"
            "- **LSH:** hashes similar vectors into similar buckets.\n"
            "- **HNSW:** builds a navigable multi-layer similarity graph.\n"
            "- **Product Quantization:** compresses vectors into cheaper representations.\n"
            "- **IVF:** clusters vectors and searches only promising clusters.\n"
            "- **Annoy:** builds multiple tree structures for candidate search.\n"
            "\n"
            "Libraries and systems combine these ideas in different ways.\n"
            "\n"
            "[[IMAGE_NEEDED: Exact k-NN versus ANN | A side-by-side diagram where "
            "exact search compares against every vector while ANN navigates only a "
            "small graph/cluster subset | Learner should notice the accuracy-versus-"
            "speed tradeoff]]\n"
            "\n"
            "---\n"
            "\n"

            "## 8. Term-based versus embedding-based retrieval\n"
            "\n"
            "Neither method is universally superior.\n"
            "\n"
            "| Property | Term-based | Embedding-based |\n"
            "|---|---|---|\n"
            "| Matching | Lexical terms | Semantic meaning |\n"
            "| Indexing | Usually cheaper/faster | Requires embedding generation |\n"
            "| Querying | Usually fast | Query embedding + vector search |\n"
            "| Strong baseline | Yes | Often needs more components |\n"
            "| Exact keywords/error codes | Often strong | Can lose important lexical details |\n"
            "| Natural-language intent | Can miss paraphrases | Often stronger |\n"
            "| Improvement path | Fewer tuning levers | Embeddings/retriever can be finetuned |\n"
            "| Cost | Usually lower | Embedding/storage/search cost can be significant |\n"
            "\n"
            "One important limitation of semantic search is that embedding a chunk "
            "can obscure exact strings such as product identifiers or error codes. "
            "This is a major reason hybrid systems are common.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. How to evaluate a retriever\n"
            "\n"
            "A retriever should be evaluated on the quality of the documents it returns.\n"
            "\n"
            "### Context precision\n"
            "\n"
            "```text\n"
            "Of everything retrieved, what fraction is relevant?\n"
            "```\n"
            "\n"
            "High precision means little irrelevant material is added to context.\n"
            "\n"
            "### Context recall\n"
            "\n"
            "```text\n"
            "Of everything relevant, what fraction did the retriever find?\n"
            "```\n"
            "\n"
            "High recall means important evidence is rarely missed.\n"
            "\n"
            "Recall is harder to measure in large real databases because you need "
            "to know the relevance of documents the retriever did **not** return.\n"
            "\n"
            "### Ranking metrics\n"
            "\n"
            "When order matters, the chapter mentions:\n"
            "\n"
            "- NDCG.\n"
            "- MAP.\n"
            "- MRR.\n"
            "\n"
            "These reward systems that place strong evidence near the top.\n"
            "\n"
            "### Evaluate the whole system too\n"
            "\n"
            "A retriever is ultimately useful if its evidence helps the generator "
            "produce better answers. Therefore evaluate:\n"
            "\n"
            "1. Retrieval quality.\n"
            "2. Embedding quality, when using embeddings.\n"
            "3. Final generated answers.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Retrieval speed, cost, and indexing tradeoffs\n"
            "\n"
            "Retrieval systems have their own engineering constraints.\n"
            "\n"
            "Embedding retrieval can add cost for:\n"
            "\n"
            "- Generating document embeddings.\n"
            "- Regenerating embeddings when data changes.\n"
            "- Vector storage.\n"
            "- Vector-search queries.\n"
            "\n"
            "Index design also creates a tradeoff:\n"
            "\n"
            "- A richer index can improve query accuracy and speed.\n"
            "- But it may require more memory and take longer to build/update.\n"
            "\n"
            "Important ANN system metrics include:\n"
            "\n"
            "- Recall.\n"
            "- Queries per second (QPS).\n"
            "- Build time.\n"
            "- Index size.\n"
            "\n"
            "A solution that retrieves well but cannot handle your update frequency "
            "or query traffic is not a good production solution.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Hybrid search, reranking, and reciprocal rank fusion\n"
            "\n"
            "Production retrieval systems often combine algorithms because lexical "
            "and semantic retrieval solve different failure modes.\n"
            "\n"
            "### Sequential combination / reranking\n"
            "\n"
            "Use a cheap retriever to get many candidates, then a more precise but "
            "expensive mechanism to rerank them.\n"
            "\n"
            "```text\n"
            "query\n"
            " -> cheap candidate retrieval\n"
            " -> expensive reranker\n"
            " -> best few chunks\n"
            "```\n"
            "\n"
            "### Parallel combination / ensemble\n"
            "\n"
            "Run multiple retrievers at the same time, then combine their rankings.\n"
            "\n"
            "### Reciprocal rank fusion (RRF)\n"
            "\n"
            "RRF gives higher weight to documents that rank near the top across "
            "retrievers. A document's final score is based on its positions in all "
            "ranked lists.\n"
            "\n"
            "The practical idea is simple:\n"
            "\n"
            "> Documents consistently ranked highly by different retrieval methods "
            "should become strong final candidates.\n"
            "\n"
            "[[IMAGE_NEEDED: Hybrid retrieval with RRF | BM25 and vector search "
            "running in parallel, producing two ranked lists that are fused into "
            "one final ranking before reranking/generation | Learner should notice "
            "how lexical and semantic evidence complement each other]]\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Chunking strategy\n"
            "\n"
            "Documents are often too large to retrieve as one unit. They are split "
            "into **chunks** before indexing.\n"
            "\n"
            "Common strategies include:\n"
            "\n"
            "- Fixed characters.\n"
            "- Fixed words.\n"
            "- Sentences.\n"
            "- Paragraphs.\n"
            "- Recursive splitting: section -> paragraph -> sentence.\n"
            "- Domain-specific splitting such as code functions or Q&A pairs.\n"
            "\n"
            "### Why overlap helps\n"
            "\n"
            "A hard boundary can split one idea across two chunks. Overlap repeats "
            "a small amount of boundary content so important context survives in at "
            "least one chunk.\n"
            "\n"
            "### Small chunks versus large chunks\n"
            "\n"
            "**Smaller chunks**\n"
            "\n"
            "- Let more different pieces fit in context.\n"
            "- Can improve retrieval specificity.\n"
            "- Increase the number of embeddings and search candidates.\n"
            "- Can lose broader context.\n"
            "\n"
            "**Larger chunks**\n"
            "\n"
            "- Preserve more local context.\n"
            "- Produce fewer index entries.\n"
            "- Can contain irrelevant material.\n"
            "- May reduce the number of distinct sources that fit in the prompt.\n"
            "\n"
            "There is no universal best chunk size or overlap. They must be evaluated "
            "for the application.\n"
            "\n"
            "[[IMAGE_NEEDED: Chunk size and overlap tradeoff | One document shown "
            "first as large chunks and then as smaller overlapping chunks | Learner "
            "should notice how overlap protects boundary information while smaller "
            "chunks increase index volume]]\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Reranking and query rewriting\n"
            "\n"
            "### Reranking\n"
            "\n"
            "The retriever's first ranking is not always the best ranking. A second "
            "stage can use a more accurate model or additional features to reorder "
            "candidates.\n"
            "\n"
            "Reranking is especially valuable when you want only a few high-quality "
            "chunks to reduce context length and cost.\n"
            "\n"
            "You can also incorporate recency when newer information should rank higher.\n"
            "\n"
            "### Query rewriting\n"
            "\n"
            "Conversational queries are often incomplete by themselves.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "User: When did John Doe last buy from us?\n"
            "Assistant: ...\n"
            "User: How about Emily Doe?\n"
            "```\n"
            "\n"
            "The final query should be rewritten into something self-contained, "
            "such as:\n"
            "\n"
            "```text\n"
            "When did Emily Doe last buy something from us?\n"
            "```\n"
            "\n"
            "A rewriter must avoid inventing missing identity information. If the "
            "query cannot be resolved safely, it should acknowledge that rather "
            "than hallucinating details.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Contextual retrieval\n"
            "\n"
            "Chunks sometimes lose the context that explains what they mean. "
            "**Contextual retrieval** enriches each chunk before indexing.\n"
            "\n"
            "Possible additions include:\n"
            "\n"
            "- Document title.\n"
            "- Summary.\n"
            "- Tags.\n"
            "- Keywords.\n"
            "- Extracted entities.\n"
            "- Product metadata or reviews.\n"
            "- Questions the chunk can answer.\n"
            "- A short generated explanation of where the chunk fits in the "
            "original document.\n"
            "\n"
            "This can help semantic retrieval recover exact concepts that might "
            "otherwise disappear during embedding.\n"
            "\n"
            "[[IMAGE_NEEDED: Contextual retrieval | A document split into chunks, "
            "each chunk receiving a short title/summary/entity context before "
            "being embedded and indexed | Learner should notice that the added "
            "context makes isolated chunks easier to retrieve correctly]]\n"
            "\n"
            "{{exercise:M06.L01.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Evaluating a retrieval solution as infrastructure\n"
            "\n"
            "Beyond relevance metrics, ask whether the retrieval platform fits the "
            "system you must operate.\n"
            "\n"
            "Important questions include:\n"
            "\n"
            "- Does it support term, vector, and hybrid search?\n"
            "- Which embedding models and ANN algorithms does it support?\n"
            "- How much data can it store?\n"
            "- What query traffic can it sustain?\n"
            "- How quickly can it index new or updated data?\n"
            "- What is its latency under realistic traffic?\n"
            "- How is managed-service pricing calculated?\n"
            "\n"
            "Enterprise applications may also require access control, compliance, "
            "and other operational features.\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Multimodal RAG\n"
            "\n"
            "RAG does not have to retrieve only text.\n"
            "\n"
            "If the generator can use images, audio, video, or other modalities, "
            "the retriever can provide those modalities as context too.\n"
            "\n"
            "For image retrieval, metadata such as captions and tags may be enough. "
            "For retrieval based on visual content, the system needs a shared "
            "multimodal embedding space.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```text\n"
            "text documents -> multimodal embeddings -> vector DB\n"
            "images         -> multimodal embeddings -> vector DB\n"
            "\n"
            "text query -> same embedding space -> nearest text + images\n"
            "```\n"
            "\n"
            "A model such as CLIP is used in the chapter as an example of mapping "
            "text and images into a joint embedding space.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. RAG with tabular data\n"
            "\n"
            "Structured tables often require a different workflow from document retrieval.\n"
            "\n"
            "Suppose a user asks:\n"
            "\n"
            "```text\n"
            "How many units of Fruity Fedora were sold in the last 7 days?\n"
            "```\n"
            "\n"
            "The system may need to:\n"
            "\n"
            "1. Understand which table and columns are relevant.\n"
            "2. Generate a SQL query.\n"
            "3. Execute the SQL.\n"
            "4. Use the result as context for the final answer.\n"
            "\n"
            "```text\n"
            "natural-language question\n"
            " -> text-to-SQL\n"
            " -> SQL execution\n"
            " -> structured result\n"
            " -> natural-language response\n"
            "```\n"
            "\n"
            "If there are too many tables to fit all schemas in the prompt, the "
            "system may first need to retrieve or predict which tables are relevant.\n"
            "\n"
            "[[IMAGE_NEEDED: Tabular RAG workflow | A pipeline showing user "
            "question -> relevant schema selection -> text-to-SQL -> database "
            "execution -> result -> response generation | Learner should notice "
            "that structured data retrieval often requires tool execution rather "
            "than nearest-neighbor document search]]\n"
            "\n"
            "---\n"
            "\n"

            "## 18. What is an agent?\n"
            "\n"
            "An agent can be understood as something that:\n"
            "\n"
            "1. Perceives an environment.\n"
            "2. Chooses actions.\n"
            "3. Acts on the environment to accomplish a goal.\n"
            "\n"
            "The environment depends on the task:\n"
            "\n"
            "- A game agent operates inside a game.\n"
            "- A coding agent operates over files, repositories, and terminals.\n"
            "- A research agent may operate over the web and document stores.\n"
            "- A robot may operate in the physical world.\n"
            "\n"
            "The model acts as the **planner/brain** that interprets the task, "
            "chooses actions, processes observations, and decides whether the goal "
            "has been reached.\n"
            "\n"
            "A simple RAG system can itself be viewed as a small agent whose "
            "retriever is one tool.\n"
            "\n"
            "[[IMAGE_NEEDED: Agent loop | A loop showing user goal -> planner -> "
            "tool/action -> environment -> observation -> planner, repeating until "
            "completion | Learner should notice that the model receives feedback "
            "from the environment rather than producing one isolated answer]]\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Why agents are harder than single-step applications\n"
            "\n"
            "Agents often need many steps. Errors compound across those steps.\n"
            "\n"
            "The chapter illustrates this with a simple multiplication intuition: "
            "even a high per-step success probability can produce poor end-to-end "
            "success across many steps.\n"
            "\n"
            "For example, with independent 95% per-step success:\n"
            "\n"
            "```text\n"
            "10 steps  -> roughly 0.95^10 ≈ 60% success\n"
            "100 steps -> roughly 0.95^100 ≈ 0.6% success\n"
            "```\n"
            "\n"
            "Agents are also higher-stakes because tools can change real systems. "
            "A wrong text answer is bad; a wrong bank transfer or database deletion "
            "can be far worse.\n"
            "\n"
            "This is why agents need careful planning, validation, permissions, "
            "reflection, observability, and human approval for risky actions.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Agent tools\n"
            "\n"
            "A tool expands what the model can perceive or do.\n"
            "\n"
            "The chapter groups useful tools into three broad categories.\n"
            "\n"
            "### 1. Knowledge augmentation\n"
            "\n"
            "Tools that provide information:\n"
            "\n"
            "- Document retrievers.\n"
            "- Image retrievers.\n"
            "- SQL readers.\n"
            "- Search APIs.\n"
            "- Email readers.\n"
            "- Slack or internal knowledge search.\n"
            "- News or web APIs.\n"
            "\n"
            "These tools help models access current or private information.\n"
            "\n"
            "### 2. Capability extension\n"
            "\n"
            "Tools that compensate for model limitations:\n"
            "\n"
            "- Calculator.\n"
            "- Unit converter.\n"
            "- Calendar/timezone tools.\n"
            "- Translator.\n"
            "- Code interpreter.\n"
            "- OCR or transcription.\n"
            "- Image-generation tools.\n"
            "\n"
            "Instead of retraining a model to do perfect arithmetic, it can call a calculator.\n"
            "\n"
            "### 3. Write actions\n"
            "\n"
            "Tools can alter the environment:\n"
            "\n"
            "- Send an email.\n"
            "- Update a database.\n"
            "- Create an order.\n"
            "- Transfer money.\n"
            "- Merge code.\n"
            "\n"
            "Write actions create the greatest automation potential and often the "
            "greatest safety risk.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Planning: turning a goal into actions\n"
            "\n"
            "A task has a **goal** and often **constraints**.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "Goal: plan a two-week trip\n"
            "Constraint: stay under a fixed budget\n"
            "```\n"
            "\n"
            "Planning means choosing a sequence of actions likely to achieve the "
            "goal while satisfying the constraints.\n"
            "\n"
            "Different valid plans can have very different efficiency. A strong "
            "planner should prefer plans that reduce unnecessary work.\n"
            "\n"
            "### Separate planning from execution\n"
            "\n"
            "If the agent creates a poor 1,000-step plan and immediately executes "
            "it, it can waste time and money before failure becomes obvious.\n"
            "\n"
            "A safer architecture is:\n"
            "\n"
            "```text\n"
            "task\n"
            " -> generate plan\n"
            " -> validate plan\n"
            " -> execute\n"
            " -> evaluate outcome\n"
            " -> replan if necessary\n"
            "```\n"
            "\n"
            "Plan validators can reject impossible actions, excessive steps, or "
            "plans that violate constraints.\n"
            "\n"
            "[[IMAGE_NEEDED: Decoupled planning and execution | A loop showing "
            "plan generation -> plan validation -> execution -> outcome evaluation "
            "-> replan, with invalid plans returning to the planner before any "
            "tool is called | Learner should notice that validation can prevent "
            "expensive or dangerous execution]]\n"
            "\n"
            "---\n"
            "\n"

            "## 22. Intent, feasibility, and human approval\n"
            "\n"
            "Understanding user intent can help an agent choose the correct tools.\n"
            "\n"
            "A support query about billing may need payment records. A password "
            "question may need documentation retrieval.\n"
            "\n"
            "An intent classifier should also recognize requests that are outside "
            "the system's scope so the agent can refuse or redirect instead of "
            "inventing a plan.\n"
            "\n"
            "Humans can participate at several stages:\n"
            "\n"
            "- Provide a high-level plan.\n"
            "- Validate a generated plan.\n"
            "- Approve risky actions.\n"
            "- Execute sensitive steps manually.\n"
            "\n"
            "The level of automation should be defined **per action**, especially "
            "for irreversible or high-impact write operations.\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Can foundation models plan?\n"
            "\n"
            "The chapter presents planning ability as an open question rather than "
            "a settled fact.\n"
            "\n"
            "Planning is fundamentally related to search:\n"
            "\n"
            "- Consider possible actions.\n"
            "- Predict resulting states.\n"
            "- Compare possible paths.\n"
            "- Backtrack when a path is poor.\n"
            "- Choose a promising path toward the goal.\n"
            "\n"
            "Autoregressive models generate forward, which creates challenges. But "
            "they can sometimes approximate backtracking through critique, revision, "
            "restarting, or an external search/state-tracking mechanism.\n"
            "\n"
            "Even if a foundation model is not a complete planner by itself, it can "
            "be one component of a larger planning system.\n"
            "\n"
            "The chapter also contrasts foundation-model agents with reinforcement-"
            "learning agents. RL usually learns a planner/policy through RL training, "
            "while an FM agent often uses the foundation model itself as the planner. "
            "The two approaches can also be combined.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Plan generation and function calling\n"
            "\n"
            "A simple planner can be built by telling the model which actions it "
            "can use and asking it to return a valid action sequence.\n"
            "\n"
            "Better planning usually comes from:\n"
            "\n"
            "- Clearer system instructions.\n"
            "- More examples.\n"
            "- Better tool descriptions.\n"
            "- Simpler tool interfaces.\n"
            "- Stronger models.\n"
            "- Finetuning for planning.\n"
            "\n"
            "### Function calling\n"
            "\n"
            "A tool is typically exposed as a function with:\n"
            "\n"
            "- A name.\n"
            "- Documentation.\n"
            "- Parameters and parameter types.\n"
            "\n"
            "A model can then return a structured tool call such as:\n"
            "\n"
            "```text\n"
            "tool: lbs_to_kg\n"
            "arguments: {\"lbs\": 40}\n"
            "```\n"
            "\n"
            "Some APIs let developers choose whether tool use is:\n"
            "\n"
            "- Required.\n"
            "- Forbidden.\n"
            "- Automatic/model-selected.\n"
            "\n"
            "Always log and inspect parameter values. A valid function name does not "
            "guarantee valid or correct arguments.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Planning granularity and hierarchical planning\n"
            "\n"
            "A detailed plan is easier to execute but harder to generate reliably. "
            "A high-level plan is easier to generate but leaves more decisions to "
            "execution time.\n"
            "\n"
            "One solution is **hierarchical planning**:\n"
            "\n"
            "```text\n"
            "high-level plan\n"
            "  -> subplan for stage 1\n"
            "  -> subplan for stage 2\n"
            "  -> ...\n"
            "```\n"
            "\n"
            "Plans can also be expressed in natural language instead of exact API "
            "function names. This makes the planner less tightly coupled to a "
            "changing tool API.\n"
            "\n"
            "A separate translator can then map a high-level action such as "
            "`retrieve product information` into an exact executable function.\n"
            "\n"
            "The tradeoff is that this translator becomes another component that "
            "must be evaluated.\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Complex agent control flows\n"
            "\n"
            "Plans do not have to be simple sequential lists.\n"
            "\n"
            "The chapter highlights four control-flow patterns:\n"
            "\n"
            "### Sequential\n"
            "\n"
            "B runs after A because B depends on A.\n"
            "\n"
            "### Parallel\n"
            "\n"
            "Independent operations run at the same time, reducing latency.\n"
            "\n"
            "### If / conditional\n"
            "\n"
            "Choose the next action based on the result of a previous action.\n"
            "\n"
            "### Loop\n"
            "\n"
            "Repeat an action until a condition is met.\n"
            "\n"
            "Non-sequential plans are more difficult for both the planner and the "
            "execution layer. When selecting an agent framework, check which control "
            "flows it supports.\n"
            "\n"
            "[[IMAGE_NEEDED: Agent control-flow patterns | Four small diagrams for "
            "sequential, parallel, conditional, and loop execution | Learner should "
            "notice that complex agents need more than a simple list of tool calls]]\n"
            "\n"
            "---\n"
            "\n"

            "## 27. Reflection and error correction\n"
            "\n"
            "Even a valid plan can fail during execution. Reflection evaluates "
            "whether the system is still on track and what should change.\n"
            "\n"
            "Reflection can happen:\n"
            "\n"
            "- Before planning: is the request feasible?\n"
            "- After plan generation: is the plan sensible?\n"
            "- After each action: did the tool produce what we expected?\n"
            "- At the end: did we actually accomplish the task?\n"
            "\n"
            "### ReAct-style loop\n"
            "\n"
            "A common pattern interleaves planning and action:\n"
            "\n"
            "```text\n"
            "Thought -> Action -> Observation\n"
            "Thought -> Action -> Observation\n"
            "...\n"
            "Finish\n"
            "```\n"
            "\n"
            "### Separate actor and evaluator\n"
            "\n"
            "Reflection can also be delegated to another model or specialized "
            "scorer. An evaluator identifies failure, and the planner uses that "
            "feedback to generate a better trajectory.\n"
            "\n"
            "The benefit is improved error correction. The cost is additional "
            "tokens, latency, and model calls.\n"
            "\n"
            "[[IMAGE_NEEDED: ReAct and reflection loop | A circular diagram showing "
            "plan/thought -> action/tool -> observation -> evaluation/reflection -> "
            "updated plan | Learner should notice that observation is fed back into "
            "future decisions rather than ignored]]\n"
            "\n"
            "---\n"
            "\n"

            "## 28. Tool selection and tool inventories\n"
            "\n"
            "More tools increase capability but also increase planning difficulty.\n"
            "\n"
            "A large tool inventory creates challenges:\n"
            "\n"
            "- Longer tool descriptions consume context.\n"
            "- Similar tools may confuse the planner.\n"
            "- More opportunities exist for invalid calls.\n"
            "\n"
            "The chapter recommends empirical tool selection.\n"
            "\n"
            "### Useful experiments\n"
            "\n"
            "- Compare different tool sets.\n"
            "- Run an **ablation study**: remove one tool and measure performance change.\n"
            "- Identify tools with high error rates.\n"
            "- Analyze which tools are used frequently or rarely.\n"
            "- Replace tools that remain difficult for the model to use correctly.\n"
            "\n"
            "Different models can prefer different tools, and different tasks can "
            "need very different inventories.\n"
            "\n"
            "### Tool transitions and reusable skills\n"
            "\n"
            "If certain tools are repeatedly used together, they may be combined "
            "into a higher-level tool. Agents can also store newly created reusable "
            "skills in a skill library for future tasks.\n"
            "\n"
            "---\n"
            "\n"

            "## 29. Agent failure modes\n"
            "\n"
            "Agents inherit normal model failures and add new failures from planning "
            "and tools.\n"
            "\n"
            "### Planning failures\n"
            "\n"
            "Examples include:\n"
            "\n"
            "- Calling a tool that does not exist.\n"
            "- Calling a valid tool with the wrong number or type of parameters.\n"
            "- Calling a valid tool with incorrect parameter values.\n"
            "- Producing a plan that does not achieve the goal.\n"
            "- Violating task constraints such as budget or location.\n"
            "- Finishing after a useful deadline.\n"
            "- Believing the task is complete when it is not.\n"
            "\n"
            "### Tool failures\n"
            "\n"
            "The planner may call the correct tool, but the tool itself returns a "
            "wrong result. A translator from high-level actions to executable calls "
            "can also fail.\n"
            "\n"
            "Another failure is simply **missing capability**: the agent does not "
            "have a tool needed for the task.\n"
            "\n"
            "Every tool should therefore be tested independently and every tool "
            "call should be observable.\n"
            "\n"
            "### Efficiency failures\n"
            "\n"
            "A successful agent can still be inefficient.\n"
            "\n"
            "Track:\n"
            "\n"
            "- Steps per completed task.\n"
            "- Cost per completed task.\n"
            "- Total time per completed task.\n"
            "- Slow or expensive actions.\n"
            "\n"
            "The appropriate baseline may be another agent or a human workflow.\n"
            "\n"
            "---\n"
            "\n"

            "## 30. How to evaluate an agent\n"
            "\n"
            "Build evaluation around the agent's actual failure modes.\n"
            "\n"
            "For a planning dataset of `(task, tool inventory)` examples, useful "
            "metrics include:\n"
            "\n"
            "- Percentage of generated plans that are valid.\n"
            "- Average number of attempts needed to obtain a valid plan.\n"
            "- Percentage of tool calls that are valid.\n"
            "- Invalid-tool call rate.\n"
            "- Invalid-parameter rate.\n"
            "- Incorrect-parameter-value rate.\n"
            "- Goal-completion rate.\n"
            "- Constraint-violation rate.\n"
            "- Cost per completed task.\n"
            "- Steps per completed task.\n"
            "- Time per completed task.\n"
            "\n"
            "Do not stop at aggregate numbers. Slice failures by task type and tool "
            "to identify patterns. A specific tool may need clearer documentation, "
            "more examples, finetuning, or replacement.\n"
            "\n"
            "{{exercise:M06.L01.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 31. Memory: internal, short-term, and long-term\n"
            "\n"
            "RAG and agents manipulate more information than can always fit into a "
            "single context window. A memory system helps retain and retrieve information.\n"
            "\n"
            "The chapter describes three major memory mechanisms.\n"
            "\n"
            "### Internal knowledge\n"
            "\n"
            "Knowledge stored in model weights through training. It is available "
            "across queries but changes only when the model changes.\n"
            "\n"
            "### Short-term memory\n"
            "\n"
            "Information placed in the current model context, such as recent "
            "messages, current plans, and observations.\n"
            "\n"
            "It is fast to access but capacity-limited.\n"
            "\n"
            "### Long-term memory\n"
            "\n"
            "External persistent information retrieved when needed. It can survive "
            "across tasks and can be updated or deleted without retraining the model.\n"
            "\n"
            "A practical allocation principle is:\n"
            "\n"
            "- Frequently needed across nearly all tasks -> internal knowledge.\n"
            "- Needed for the current task -> short-term memory.\n"
            "- Occasionally needed or persistent -> long-term memory.\n"
            "\n"
            "[[IMAGE_NEEDED: Three-level AI memory hierarchy | A hierarchy showing "
            "model weights as internal knowledge, active context as short-term "
            "memory, and external persistent stores as long-term memory | Learner "
            "should notice the tradeoff between persistence, capacity, and access]]\n"
            "\n"
            "---\n"
            "\n"

            "## 32. Why memory matters\n"
            "\n"
            "Memory can help an application:\n"
            "\n"
            "### Manage information overflow\n"
            "\n"
            "Move information that no longer fits in active context into external memory.\n"
            "\n"
            "### Persist across sessions\n"
            "\n"
            "Remember user preferences, previous work, history, or project state.\n"
            "\n"
            "### Improve consistency\n"
            "\n"
            "Referencing earlier decisions can help the model stay consistent over time.\n"
            "\n"
            "### Preserve structure\n"
            "\n"
            "External memory can store structured artifacts such as tables, queues, "
            "and files without flattening everything into unstructured context text.\n"
            "\n"
            "---\n"
            "\n"

            "## 33. Memory management\n"
            "\n"
            "A memory system needs two broad functions:\n"
            "\n"
            "1. **Memory management:** decide what to store, merge, replace, or remove.\n"
            "2. **Memory retrieval:** fetch long-term information relevant to the current task.\n"
            "\n"
            "Retrieving long-term memory is essentially another RAG problem.\n"
            "\n"
            "### Moving overflow out of short-term memory\n"
            "\n"
            "Part of the context window may be reserved for information retrieved "
            "from long-term memory. The remaining capacity holds active short-term memory.\n"
            "\n"
            "When active memory exceeds the allocated capacity, some information "
            "must be compressed, moved, or discarded.\n"
            "\n"
            "### FIFO is simple but risky\n"
            "\n"
            "First-in-first-out removes the oldest context first. It is easy to "
            "implement but can discard the most important information—for example, "
            "the original goal stated at the beginning of a long conversation.\n"
            "\n"
            "### Summarization\n"
            "\n"
            "Compress older history into a summary while preserving key entities, "
            "constraints, and decisions.\n"
            "\n"
            "### Reflection-based memory updates\n"
            "\n"
            "After new information arrives, an agent can decide whether it should:\n"
            "\n"
            "- Be inserted as a new memory.\n"
            "- Be merged with an existing memory.\n"
            "- Replace outdated information.\n"
            "- Be ignored.\n"
            "\n"
            "Contradictions require an application-specific policy. Keeping only the "
            "newest fact may be correct in one system and dangerous in another.\n"
            "\n"
            "[[IMAGE_NEEDED: Memory management flow | New observation entering a "
            "decision node with branches insert, merge, replace, ignore, plus "
            "retrieval from long-term memory back into active context | Learner "
            "should notice that useful memory requires active management, not only storage]]\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1\n"
            "\n"
            "> A very large context window makes retrieval unnecessary.\n"
            "\n"
            "**Why this is wrong:** data can exceed any fixed context, irrelevant "
            "tokens add cost and latency, and models do not always use long context efficiently.\n"
            "\n"
            "### Misconception 2\n"
            "\n"
            "> Vector search is always better than BM25.\n"
            "\n"
            "**Why this is wrong:** BM25 can be fast, cheap, and excellent for exact "
            "terms, while semantic search helps with meaning and paraphrases. "
            "Production systems often combine both.\n"
            "\n"
            "### Misconception 3\n"
            "\n"
            "> Once the retriever is good, the whole RAG system is good.\n"
            "\n"
            "**Why this is wrong:** retrieval, embeddings, prompt construction, and "
            "generation all affect end-to-end quality.\n"
            "\n"
            "### Misconception 4\n"
            "\n"
            "> Smaller chunks are always better because they are more precise.\n"
            "\n"
            "**Why this is wrong:** overly small chunks can lose essential context "
            "and greatly increase embedding/storage/search overhead.\n"
            "\n"
            "### Misconception 5\n"
            "\n"
            "> Giving an agent more tools always improves it.\n"
            "\n"
            "**Why this is wrong:** larger inventories make tool selection harder, "
            "consume context, and create more opportunities for incorrect calls.\n"
            "\n"
            "### Misconception 6\n"
            "\n"
            "> A valid tool call means the agent made the right decision.\n"
            "\n"
            "**Why this is wrong:** the function can be valid while parameters are "
            "wrong or the entire chosen action is inappropriate for the goal.\n"
            "\n"
            "### Misconception 7\n"
            "\n"
            "> If the final answer is correct, agent evaluation is complete.\n"
            "\n"
            "**Why this is wrong:** cost, latency, excessive steps, unsafe actions, "
            "invalid calls, and tool failures can still make the system unsuitable.\n"
            "\n"
            "### Misconception 8\n"
            "\n"
            "> Memory means keeping the entire conversation forever in the prompt.\n"
            "\n"
            "**Why this is wrong:** useful memory requires selective storage, "
            "compression, retrieval, and lifecycle management.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| RAG | Retrieval-augmented generation; retrieve external information before generation. |\n"
            "| Retriever | Component that ranks and fetches information relevant to a query. |\n"
            "| Generator | Model that produces the final response using the query and retrieved context. |\n"
            "| Indexing | Preparing data so it can be retrieved efficiently later. |\n"
            "| Querying | Retrieving and ranking information for a specific request. |\n"
            "| TF | Term frequency: how often a term appears in a document. |\n"
            "| IDF | Inverse document frequency: measure of how rare/informative a term is across documents. |\n"
            "| TF-IDF | Lexical relevance score combining local term frequency and global rarity. |\n"
            "| Inverted index | Mapping from terms to documents that contain them. |\n"
            "| BM25 | Widely used lexical ranking algorithm derived from TF-IDF-style ideas. |\n"
            "| Semantic retrieval | Retrieval based on embedding similarity rather than exact word overlap. |\n"
            "| Vector database | Store/index designed to support vector similarity search. |\n"
            "| k-NN | Exact nearest-neighbor retrieval by comparing against candidate vectors. |\n"
            "| ANN | Approximate nearest-neighbor search for faster large-scale vector retrieval. |\n"
            "| HNSW | Graph-based ANN indexing/search approach. |\n"
            "| IVF | Cluster-based candidate-selection approach for vector search. |\n"
            "| Product Quantization | Vector-compression method that reduces search/storage cost. |\n"
            "| Context precision | Fraction of retrieved documents that are relevant. |\n"
            "| Context recall | Fraction of all relevant documents that were retrieved. |\n"
            "| MRR | Mean Reciprocal Rank; ranking metric emphasizing the position of the first relevant result. |\n"
            "| Hybrid search | Combining lexical and embedding-based retrieval. |\n"
            "| Reranking | Reordering initially retrieved candidates using a more precise mechanism. |\n"
            "| RRF | Reciprocal rank fusion; combines multiple ranked lists. |\n"
            "| Chunking | Splitting source documents into retrievable units. |\n"
            "| Query rewriting | Turning an ambiguous/context-dependent query into a self-contained retrieval query. |\n"
            "| Contextual retrieval | Enriching chunks with metadata/context before indexing. |\n"
            "| Multimodal RAG | Retrieving context across modalities such as text and images. |\n"
            "| Text-to-SQL | Converting a natural-language request into SQL for structured-data retrieval. |\n"
            "| Agent | System that perceives an environment and chooses actions to achieve a goal. |\n"
            "| Tool inventory | Set of external actions/functions available to an agent. |\n"
            "| Function calling | Model-generated structured invocation of an external tool. |\n"
            "| Planning | Choosing a sequence/control flow of actions to accomplish a goal under constraints. |\n"
            "| Reflection | Evaluating plans/actions/outcomes to detect errors and improve subsequent behavior. |\n"
            "| ReAct | Pattern interleaving reasoning/planning, actions, and observations. |\n"
            "| Ablation study | Removing a component/tool and measuring the resulting performance change. |\n"
            "| Internal knowledge | Information encoded in model parameters. |\n"
            "| Short-term memory | Active information stored in the current model context. |\n"
            "| Long-term memory | Persistent external information retrieved when needed. |\n"
            "| FIFO | First-in-first-out memory policy that removes the oldest items first. |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. What is the difference between instructions and query-specific context?\n"
            "2. Why can RAG remain useful even with a very large context window?\n"
            "3. What are the retriever's indexing and querying responsibilities?\n"
            "4. How do TF and IDF capture different aspects of term relevance?\n"
            "5. Why does BM25 normalize for document length?\n"
            "6. What retrieval problems can exact keywords solve better than embeddings?\n"
            "7. What additional indexing step is required for embedding-based retrieval?\n"
            "8. Why is exact k-NN too expensive for large databases?\n"
            "9. What tradeoff does ANN make?\n"
            "10. At a high level, how do HNSW, IVF, and product quantization differ?\n"
            "11. What is the difference between context precision and context recall?\n"
            "12. Why is recall difficult to measure in a large production corpus?\n"
            "13. Why should RAG be evaluated both component-by-component and end-to-end?\n"
            "14. Why can vector-database cost become significant?\n"
            "15. What is hybrid search?\n"
            "16. What problem does RRF solve?\n"
            "17. What are the advantages and disadvantages of smaller chunks?\n"
            "18. Why is overlap used during chunking?\n"
            "19. When is query rewriting necessary?\n"
            "20. What does contextual retrieval add to a chunk?\n"
            "21. How does multimodal RAG retrieve images from a text query?\n"
            "22. How does tabular RAG differ from normal document RAG?\n"
            "23. Define an agent using environment and actions.\n"
            "24. What are the three tool categories discussed in this lesson?\n"
            "25. Why do agent errors compound over many steps?\n"
            "26. Why should planning often be separated from execution?\n"
            "27. Where can humans intervene in an agent workflow?\n"
            "28. What is function calling?\n"
            "29. Why should function-call parameter values be logged?\n"
            "30. What is the planning granularity tradeoff?\n"
            "31. What is hierarchical planning?\n"
            "32. What four control-flow patterns were introduced?\n"
            "33. What role does reflection play after a tool returns an observation?\n"
            "34. How does ReAct connect planning and execution?\n"
            "35. Why can removing a tool improve an agent?\n"
            "36. Name three planning/tool failure metrics for agent evaluation.\n"
            "37. Why is agent efficiency an evaluation criterion even when the task succeeds?\n"
            "38. Distinguish internal, short-term, and long-term memory.\n"
            "39. Why can FIFO memory removal be dangerous?\n"
            "40. How can summarization and reflection improve memory management?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**RAG and agents are two ways of giving a foundation model the "
            "information and capabilities it does not already have in its immediate "
            "context. Reliable systems do not stop at connecting a model to a "
            "vector database or a list of tools: they engineer retrieval, planning, "
            "validation, execution, reflection, evaluation, permissions, and memory "
            "as one observable system.**\n"
        ),

        "estimated_minutes": 330,

        "has_code_examples": False,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "context-construction", "title": "Context construction", "order": 1},
            {"id": "rag-basics", "title": "RAG basics", "order": 2},
            {"id": "rag-architecture", "title": "RAG architecture", "order": 3},
            {"id": "term-retrieval", "title": "Term-based retrieval", "order": 4},
            {"id": "term-tokenization", "title": "Tokenization for lexical retrieval", "order": 5},
            {"id": "embedding-retrieval", "title": "Embedding-based retrieval", "order": 6},
            {"id": "vector-search", "title": "Vector search", "order": 7},
            {"id": "retrieval-comparison", "title": "Compare retrieval algorithms", "order": 8},
            {"id": "retrieval-evaluation", "title": "Retriever evaluation", "order": 9},
            {"id": "retrieval-performance", "title": "Retrieval speed and cost", "order": 10},
            {"id": "hybrid-search", "title": "Hybrid search and RRF", "order": 11},
            {"id": "chunking", "title": "Chunking strategy", "order": 12},
            {"id": "reranking-query-rewriting", "title": "Reranking and query rewriting", "order": 13},
            {"id": "contextual-retrieval", "title": "Contextual retrieval", "order": 14},
            {"id": "retrieval-solution-selection", "title": "Evaluate retrieval infrastructure", "order": 15},
            {"id": "multimodal-rag", "title": "Multimodal RAG", "order": 16},
            {"id": "tabular-rag", "title": "RAG with tabular data", "order": 17},
            {"id": "agent-overview", "title": "Agent overview", "order": 18},
            {"id": "compound-errors", "title": "Compound agent errors", "order": 19},
            {"id": "agent-tools", "title": "Agent tools", "order": 20},
            {"id": "planning", "title": "Planning", "order": 21},
            {"id": "intent-human-approval", "title": "Intent and human approval", "order": 22},
            {"id": "planning-models", "title": "Foundation models as planners", "order": 23},
            {"id": "plan-generation", "title": "Plan generation and function calling", "order": 24},
            {"id": "planning-granularity", "title": "Planning granularity", "order": 25},
            {"id": "control-flows", "title": "Agent control flows", "order": 26},
            {"id": "reflection", "title": "Reflection and error correction", "order": 27},
            {"id": "tool-selection", "title": "Tool selection", "order": 28},
            {"id": "agent-failures", "title": "Agent failure modes", "order": 29},
            {"id": "agent-evaluation", "title": "Agent evaluation", "order": 30},
            {"id": "memory-types", "title": "Memory types", "order": 31},
            {"id": "memory-benefits", "title": "Why memory matters", "order": 32},
            {"id": "memory-management", "title": "Memory management", "order": 33},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M06.L01.EX01",

            "title": "Design a Production RAG Retriever",

            "lesson_code": "M06.L01",

            "section_id": "contextual-retrieval",

            "placement": "after_section",

            "description": (
                "Design a retriever for a realistic knowledge base and justify "
                "the choices using the retrieval concepts in this lesson."
            ),

            "instructions": (
                "Imagine you are building a support assistant over 100,000 product "
                "manuals, support tickets, and troubleshooting notes.\n\n"
                "1. Decide what should be indexed as a chunk and propose an initial "
                "chunk size/overlap strategy.\n"
                "2. Explain what information should be stored as metadata.\n"
                "3. Choose term-based, embedding-based, or hybrid retrieval and "
                "justify your choice.\n"
                "4. If you use semantic retrieval, explain what must be evaluated "
                "about the embedding model.\n"
                "5. Explain whether you would use exact k-NN or ANN at this scale.\n"
                "6. Choose one ANN style from HNSW, IVF, LSH, product quantization, "
                "or Annoy and explain the tradeoff you care about.\n"
                "7. Design a reranking stage.\n"
                "8. Give one example of a conversation that requires query rewriting.\n"
                "9. Explain how contextual retrieval could improve one isolated chunk.\n"
                "10. Define context precision, context recall, and one ranking metric "
                "for your evaluation set.\n"
                "11. Define two infrastructure metrics such as QPS, build time, "
                "index size, or query latency.\n"
                "12. Explain how you would evaluate the RAG system end to end."
            ),

            "expected_output": (
                "A compact RAG architecture and evaluation plan that covers "
                "chunking, indexing, retrieval choice, vector-search tradeoffs, "
                "reranking, rewriting, contextualization, and end-to-end metrics."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "rag-design",
                "retrieval-selection",
                "chunking",
                "vector-search",
                "hybrid-retrieval",
                "retrieval-evaluation",
            ],
        },

        {
            "id": "M06.L01.EX02",

            "title": "Design and Evaluate a Tool-Using Agent",

            "lesson_code": "M06.L01",

            "section_id": "agent-evaluation",

            "placement": "after_section",

            "description": (
                "Build a safe planning and evaluation design for a multi-step "
                "agent rather than treating tool calling as a single model prompt."
            ),

            "instructions": (
                "Design an agent that receives the task: 'Prepare a weekly sales "
                "report and email it to the sales manager.'\n\n"
                "1. Define the environment and the agent's goal/constraints.\n"
                "2. Propose a minimal tool inventory.\n"
                "3. Classify each tool as read-only or write-capable.\n"
                "4. Mark which actions require human approval.\n"
                "5. Create a high-level plan before tool-specific execution.\n"
                "6. Identify which steps can run in parallel and which must be sequential.\n"
                "7. Define a plan-validation step before execution.\n"
                "8. Add reflection after at least two important tool calls.\n"
                "9. Define what should happen if a tool fails or returns incomplete data.\n"
                "10. Define at least six agent-evaluation metrics, including goal "
                "success, invalid calls, parameter errors, steps, cost, and latency.\n"
                "11. Describe one ablation experiment for the tool inventory.\n"
                "12. Define what information belongs in short-term versus long-term memory."
            ),

            "expected_output": (
                "An agent architecture showing tools, planning, validation, "
                "permissions, reflection, failure handling, memory, and measurable "
                "evaluation criteria."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "agent-design",
                "tool-use",
                "planning",
                "reflection",
                "human-in-the-loop",
                "agent-evaluation",
                "memory-design",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M06.L01.QZ01",

        "title": "RAG and Agents — Knowledge Check",

        "lesson_code": "M06.L01",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M06.L01.Q01",
                "section_id": "rag-basics",
                "question": "What is the central purpose of RAG?",
                "options": [
                    "Retrieve query-relevant external information before generation",
                    "Increase the model's parameter count at inference time",
                    "Replace the generator with a database",
                    "Remove the need for context",
                ],
                "correct": 0,
                "explanation": (
                    "RAG constructs query-specific context by retrieving useful "
                    "information from external memory before generation."
                ),
            },
            {
                "id": "M06.L01.Q02",
                "section_id": "term-retrieval",
                "question": "What does IDF try to capture?",
                "options": [
                    "How rare and therefore informative a term is across documents",
                    "How many embeddings a vector database stores",
                    "How long a generated answer is",
                    "The number of transformer layers",
                ],
                "correct": 0,
                "explanation": (
                    "Terms appearing in fewer documents receive greater importance "
                    "than ubiquitous terms."
                ),
            },
            {
                "id": "M06.L01.Q03",
                "section_id": "embedding-retrieval",
                "question": (
                    "Why must the query and indexed documents use compatible "
                    "embedding representations?"
                ),
                "options": [
                    "Similarity search is meaningful only when vectors live in a "
                    "compatible embedding space",
                    "Vector databases accept only one query per day",
                    "BM25 requires embeddings",
                    "Query rewriting changes model weights",
                ],
                "correct": 0,
                "explanation": (
                    "Nearest-neighbor retrieval compares vectors, so they must be "
                    "produced in a compatible semantic space."
                ),
            },
            {
                "id": "M06.L01.Q04",
                "section_id": "vector-search",
                "question": "Why use ANN instead of exact k-NN on a large vector store?",
                "options": [
                    "To trade a small amount of exactness for much faster search",
                    "To eliminate embeddings",
                    "To guarantee perfect recall at zero cost",
                    "To convert vectors back into documents",
                ],
                "correct": 0,
                "explanation": (
                    "Exact comparison against every vector becomes expensive at "
                    "scale; ANN reduces the search space."
                ),
            },
            {
                "id": "M06.L01.Q05",
                "section_id": "retrieval-evaluation",
                "question": "What does context precision measure?",
                "options": [
                    "The fraction of retrieved items that are relevant",
                    "The fraction of all relevant items that were retrieved",
                    "The number of chunks in the database",
                    "The generator's token accuracy",
                ],
                "correct": 0,
                "explanation": (
                    "Precision asks how much of what you retrieved is actually useful."
                ),
            },
            {
                "id": "M06.L01.Q06",
                "section_id": "hybrid-search",
                "question": "Why combine BM25 and semantic retrieval?",
                "options": [
                    "They capture complementary lexical and semantic signals",
                    "They are mathematically identical",
                    "BM25 is required for vector storage",
                    "Hybrid search removes the need for evaluation",
                ],
                "correct": 0,
                "explanation": (
                    "Lexical systems are strong for exact terms while embedding "
                    "retrieval can capture paraphrases and meaning."
                ),
            },
            {
                "id": "M06.L01.Q07",
                "section_id": "chunking",
                "question": "What is a major risk of making chunks too small?",
                "options": [
                    "Important surrounding context can be lost",
                    "The number of chunks always decreases",
                    "The embedding model becomes deterministic",
                    "Query rewriting becomes unnecessary",
                ],
                "correct": 0,
                "explanation": (
                    "Smaller chunks can isolate facts from the context required to "
                    "understand or retrieve them."
                ),
            },
            {
                "id": "M06.L01.Q08",
                "section_id": "reranking-query-rewriting",
                "question": (
                    "Why should 'How about Emily Doe?' often be rewritten before retrieval?"
                ),
                "options": [
                    "The query depends on earlier conversational context",
                    "Embedding models cannot process names",
                    "BM25 rejects short queries",
                    "The generator requires SQL",
                ],
                "correct": 0,
                "explanation": (
                    "The short follow-up is ambiguous by itself, so rewriting makes "
                    "the user's intended question explicit."
                ),
            },
            {
                "id": "M06.L01.Q09",
                "section_id": "tabular-rag",
                "question": (
                    "Which workflow is most appropriate when a question requires "
                    "aggregating rows from a relational table?"
                ),
                "options": [
                    "Generate SQL -> execute SQL -> use result to generate answer",
                    "Embed the entire database as one text chunk only",
                    "Use lexical search without database execution",
                    "Increase temperature",
                ],
                "correct": 0,
                "explanation": (
                    "Structured data often requires semantic parsing/text-to-SQL "
                    "and execution rather than document similarity alone."
                ),
            },
            {
                "id": "M06.L01.Q10",
                "section_id": "agent-overview",
                "question": "What two ideas fundamentally characterize an agent?",
                "options": [
                    "Its environment and the actions it can perform",
                    "Its parameter count and tokenizer",
                    "Its benchmark rank and temperature",
                    "Its embedding dimension and chunk size",
                ],
                "correct": 0,
                "explanation": (
                    "An agent perceives an environment and takes actions in that "
                    "environment to accomplish goals."
                ),
            },
            {
                "id": "M06.L01.Q11",
                "section_id": "compound-errors",
                "question": (
                    "Why can a high per-step success rate still produce a weak "
                    "multi-step agent?"
                ),
                "options": [
                    "Errors compound across many dependent steps",
                    "Agents cannot use tools",
                    "Every step resets the model weights",
                    "RAG removes all uncertainty",
                ],
                "correct": 0,
                "explanation": (
                    "The probability that every step succeeds falls as the number "
                    "of required steps increases."
                ),
            },
            {
                "id": "M06.L01.Q12",
                "section_id": "planning",
                "question": (
                    "Why is it often safer to validate a plan before executing it?"
                ),
                "options": [
                    "Invalid or wasteful plans can be rejected before expensive or "
                    "dangerous actions occur",
                    "Plan validation guarantees perfect reasoning",
                    "Execution cannot produce observations",
                    "Tools work only after two model calls",
                ],
                "correct": 0,
                "explanation": (
                    "Separating plan generation from execution allows impossible, "
                    "unsafe, or excessive plans to be caught early."
                ),
            },
            {
                "id": "M06.L01.Q13",
                "section_id": "plan-generation",
                "question": "What is function calling?",
                "options": [
                    "The model selecting a structured external function/tool invocation",
                    "Changing the model's weights during every query",
                    "Embedding every tool name in a vector database",
                    "Only executing Python code",
                ],
                "correct": 0,
                "explanation": (
                    "Function calling exposes structured tools and lets the model "
                    "select a tool and its arguments."
                ),
            },
            {
                "id": "M06.L01.Q14",
                "section_id": "reflection",
                "question": (
                    "What is the purpose of reflection in an agent workflow?"
                ),
                "options": [
                    "Evaluate plans/actions/outcomes and guide correction",
                    "Increase vocabulary size",
                    "Replace all tools with one tool",
                    "Remove observations from the context",
                ],
                "correct": 0,
                "explanation": (
                    "Reflection identifies whether the agent is on track and what "
                    "should be corrected or replanned."
                ),
            },
            {
                "id": "M06.L01.Q15",
                "section_id": "tool-selection",
                "question": "What does a tool ablation study test?",
                "options": [
                    "How performance changes when a tool is removed",
                    "How many tokens the tool name contains",
                    "Whether the model can finetune itself",
                    "Whether two embeddings are identical",
                ],
                "correct": 0,
                "explanation": (
                    "If removing a tool does not hurt performance, the tool may not "
                    "be worth the complexity it adds."
                ),
            },
            {
                "id": "M06.L01.Q16",
                "section_id": "agent-evaluation",
                "question": (
                    "Which metric directly detects a planner that frequently calls "
                    "functions that are not in its inventory?"
                ),
                "options": [
                    "Invalid-tool call rate",
                    "Context recall",
                    "Embedding cosine similarity",
                    "Index build time",
                ],
                "correct": 0,
                "explanation": (
                    "Invalid-tool call rate measures how often the planner invents "
                    "or selects unavailable tools."
                ),
            },
            {
                "id": "M06.L01.Q17",
                "section_id": "memory-types",
                "question": (
                    "Which memory mechanism is best described as persistent "
                    "external information retrieved when needed?"
                ),
                "options": [
                    "Long-term memory",
                    "Short-term context",
                    "Internal model knowledge",
                    "Sampling temperature",
                ],
                "correct": 0,
                "explanation": (
                    "Long-term memory is stored externally and can persist across tasks."
                ),
            },
            {
                "id": "M06.L01.Q18",
                "section_id": "memory-management",
                "type": "open",
                "question": (
                    "Design a memory policy for a long-running AI assistant. Explain "
                    "what you would keep in short-term memory, what you would move "
                    "to long-term memory, how you would compress old conversation "
                    "history, and how you would resolve conflicting old and new information."
                ),
            },
        ],

        "passing_score": 70,
    },
}
