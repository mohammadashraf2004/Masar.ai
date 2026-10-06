"""M01.L06 — Working with Memory and Knowledge RAG for Agents.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
AI Agents in Action, Chapter 6, page range not supplied in the provided source.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel


# ---------------------------------------------------------------------------
# Lesson metadata
# ---------------------------------------------------------------------------

LESSON_CODE = "M01.L06"

MODULE_ORDER = 1

MODULE_TITLE = "Foundations of AI Agents"

MODULE_DESCRIPTION = (
    "Learn how agents retrieve external knowledge and past experience using "
    "RAG, vector search, hybrid retrieval, structured databases, graph memory, "
    "MCP memory services, grounding, compression, and forgetting."
)

SOURCE_CHAPTER = 6

SOURCE_PAGES = "Page range not supplied in the provided chapter text"


# ---------------------------------------------------------------------------
# Topic
# ---------------------------------------------------------------------------

TOPIC = {
    "title": "Working with Memory and Knowledge RAG for Agents",

    "slug": "ai-agents-m01-l06",

    "description": (
        "Build a practical mental model of retrieval-augmented generation and "
        "agent memory, from TF-IDF and embeddings to vector databases, hybrid "
        "search, grounding, graph memory, MCP, and memory maintenance."
    ),

    "order": 6,

    "difficulty": DifficultyLevel.beginner,

    "estimated_hours": 4.25,

    "skill_tags": [
        "rag",
        "retrieval",
        "vector-search",
        "embeddings",
        "tf-idf",
        "cosine-similarity",
        "chromadb",
        "hybrid-search",
        "rrf",
        "grounding",
        "agent-memory",
        "graph-memory",
        "mcp",
        "memory-compression",
        "module-01",
    ],

    "prerequisite_ids": [
        "M01.L01",
        "M01.L02",
        "M01.L03",
        "M01.L04",
        "M01.L05",
    ],


    # =======================================================================
    # LESSON
    # =======================================================================

    "lesson": {
        "title": "Working with Memory and Knowledge RAG for Agents",

        "content": (
            "# Working with Memory and Knowledge RAG for Agents\n"
            "\n"
            "> **Course:** AI Agents  \n"
            "> **Lesson:** M01.L06  \n"
            "> **Module:** Foundations of AI Agents  \n"
            "> **Source alignment:** *AI Agents in Action*, Chapter 6. "
            "The supplied chapter did not include a page range. This lesson is an "
            "instructor-authored curriculum adaptation rather than a reproduction "
            "of the source text.\n"
            "\n"
            "---\n"
            "\n"

            "## Learning outcomes\n"
            "\n"
            "By the end of this lesson, you should be able to:\n"
            "\n"
            "- Explain why agents need retrieval beyond the model's training data.\n"
            "- Distinguish **knowledge** from **memory**.\n"
            "- Explain retrieval, augmentation, and retrieval-augmented generation (RAG).\n"
            "- Describe the ingestion and retrieval phases of a RAG pipeline.\n"
            "- Explain the difference between keyword search and semantic search.\n"
            "- Calculate and interpret basic TF-IDF values.\n"
            "- Explain cosine similarity and cosine distance.\n"
            "- Describe what neural text embeddings represent.\n"
            "- Explain how a vector database performs similarity search.\n"
            "- Build the conceptual pipeline for ChromaDB-based retrieval.\n"
            "- Explain why vector search alone can miss exact codes, numbers, and relationships.\n"
            "- Compare keyword, vector, hybrid, relational, and graph retrieval.\n"
            "- Explain Reciprocal Rank Fusion (RRF) at a practical level.\n"
            "- Build the architecture of a grounded RAG agent.\n"
            "- Explain strong versus weak grounding.\n"
            "- Describe working memory and persistent agent memory.\n"
            "- Explain graph memory, semantic memory, and hybrid memory.\n"
            "- Explain memory augmentation, compression, and forgetting.\n"
            "- Identify additional requirements for production-grade memory systems.\n"
            "\n"
            "---\n"
            "\n"

            "## 1. Why agents need retrieval\n"
            "\n"
            "An LLM can only directly use what is available in its model parameters and current "
            "context. That creates immediate limits for real agents.\n"
            "\n"
            "An agent may need to answer questions about:\n"
            "\n"
            "- a document uploaded recently,\n"
            "- an internal company policy,\n"
            "- a private codebase,\n"
            "- current structured data,\n"
            "- an earlier conversation,\n"
            "- a preference the user shared last week.\n"
            "\n"
            "None of these should be assumed to exist inside the model's training data.\n"
            "\n"
            "Retrieval solves this by searching information stored **outside** the LLM and bringing "
            "only relevant pieces into the current model call.\n"
            "\n"
            "This gives us a fundamental architecture:\n"
            "\n"
            "```text\n"
            "Large external store\n"
            "      |\n"
            "      | retrieve relevant items\n"
            "      v\n"
            "Current context window\n"
            "      |\n"
            "      v\n"
            "LLM / Agent\n"
            "```\n"
            "\n"
            "External storage may grow independently, while each individual LLM call remains bounded "
            "by a finite context window.\n"
            "\n"
            "[[IMAGE_NEEDED: External storage versus bounded context | "
            "Show a large database/vector store containing many documents and memories on the left, "
            "a retrieval filter in the middle, and a small context window feeding an LLM on the right | "
            "Learner should notice that retrieval selects a small relevant subset from a much larger store]]\n"
            "\n"
            "---\n"
            "\n"

            "## 2. Knowledge and memory are siblings, not twins\n"
            "\n"
            "Knowledge and memory often use the same retrieval technologies, but they represent different things.\n"
            "\n"
            "### Knowledge\n"
            "\n"
            "Knowledge is external information the agent consults.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- PDFs,\n"
            "- manuals,\n"
            "- policies,\n"
            "- database tables,\n"
            "- code repositories,\n"
            "- product catalogs.\n"
            "\n"
            "### Memory\n"
            "\n"
            "Memory comes from prior experience or interaction.\n"
            "\n"
            "Examples:\n"
            "\n"
            "- previous conversation turns,\n"
            "- earlier agent actions,\n"
            "- recorded user preferences,\n"
            "- prior task outcomes,\n"
            "- observed relationships.\n"
            "\n"
            "| Property | Knowledge | Memory |\n"
            "|---|---|---|\n"
            "| Main source | External information | Interaction and experience |\n"
            "| Typical update | When source changes | During ongoing use |\n"
            "| Example | Company policy PDF | User prefers concise summaries |\n"
            "| Retrieval | Vector, keyword, SQL, graph | Same retrieval families |\n"
            "\n"
            "The storage mechanisms overlap. The meaning and lifecycle of the stored information differ.\n"
            "\n"
            "---\n"
            "\n"

            "## 3. Retrieval and augmentation\n"
            "\n"
            "Two operations form the foundation of RAG.\n"
            "\n"
            "### Retrieval\n"
            "\n"
            "Search an external source for information relevant to the current query or task.\n"
            "\n"
            "### Augmentation\n"
            "\n"
            "Insert the retrieved information into the model's current context so the model can use it.\n"
            "\n"
            "Together:\n"
            "\n"
            "```text\n"
            "User query\n"
            "   |\n"
            "   v\n"
            "Retrieve relevant information\n"
            "   |\n"
            "   v\n"
            "Augment prompt/context\n"
            "   |\n"
            "   v\n"
            "LLM generates grounded response\n"
            "```\n"
            "\n"
            "This is **retrieval-augmented generation (RAG)**.\n"
            "\n"
            "The same high-level mechanism can retrieve document knowledge or previous memories.\n"
            "\n"
            "---\n"
            "\n"

            "## 4. The two phases of a RAG system\n"
            "\n"
            "The chapter separates RAG into **ingestion** and **retrieval**.\n"
            "\n"
            "### Phase A — Ingestion\n"
            "\n"
            "```text\n"
            "Documents\n"
            "  -> load\n"
            "  -> split/chunk\n"
            "  -> embed\n"
            "  -> store vectors + source data\n"
            "```\n"
            "\n"
            "### Phase B — Retrieval and generation\n"
            "\n"
            "```text\n"
            "User query\n"
            "  -> embed query\n"
            "  -> search vector store\n"
            "  -> retrieve relevant chunks\n"
            "  -> add chunks to prompt\n"
            "  -> LLM answers\n"
            "```\n"
            "\n"
            "A critical distinction is that the **embedding model** and the **generative LLM** perform "
            "different jobs.\n"
            "\n"
            "- Embedder: maps text into vectors for retrieval.\n"
            "- LLM: reasons over retrieved context and generates the answer.\n"
            "\n"
            "[[IMAGE_NEEDED: RAG ingestion and retrieval phases | "
            "Two-column diagram. Ingestion: Document -> Chunk -> Embedding Model -> Vector DB. "
            "Retrieval: Query -> Embedding -> Similarity Search -> Retrieved Chunks -> LLM -> Answer | "
            "Learner should clearly see that embedding and generation are separate operations]]\n"
            "\n"
            "---\n"
            "\n"

            "## 5. Semantic search: retrieve by meaning\n"
            "\n"
            "Traditional keyword search looks for literal terms. Semantic search attempts to match "
            "the **meaning** of the query to the meaning of stored content.\n"
            "\n"
            "For example:\n"
            "\n"
            "```text\n"
            "Query: vehicles\n"
            "Document: cars need regular maintenance\n"
            "```\n"
            "\n"
            "A pure word-matching system may miss the document because `vehicles` and `cars` are "
            "different words. A semantic embedding system may place them close together in vector space.\n"
            "\n"
            "This is powerful, but similarity is not truth.\n"
            "\n"
            "The chapter highlights three practical limitations:\n"
            "\n"
            "1. A semantically similar result may still be factually wrong.\n"
            "2. Top-K retrieval can discard relevant information outside the selected K results.\n"
            "3. Approximate nearest-neighbor search trades a small amount of exactness for speed.\n"
            "\n"
            "So retrieval quality still needs evaluation.\n"
            "\n"
            "---\n"
            "\n"

            "## 6. Start simple: TF-IDF\n"
            "\n"
            "Before neural embeddings, the chapter introduces TF-IDF because its mechanics are easy to understand.\n"
            "\n"
            "**TF-IDF** stands for **Term Frequency–Inverse Document Frequency**.\n"
            "\n"
            "It gives a higher weight to terms that are important in one document but not common across every document.\n"
            "\n"
            "### Term Frequency (TF)\n"
            "\n"
            "For the sentence:\n"
            "\n"
            "```text\n"
            "The sky is blue and beautiful\n"
            "```\n"
            "\n"
            "If `blue` appears once among six words:\n"
            "\n"
            "```text\n"
            "TF(blue) = 1 / 6 ≈ 0.167\n"
            "```\n"
            "\n"
            "### Inverse Document Frequency (IDF)\n"
            "\n"
            "If the corpus has eight documents and four contain `blue`:\n"
            "\n"
            "```text\n"
            "IDF(blue) = log10(8 / 4)\n"
            "          ≈ 0.301\n"
            "```\n"
            "\n"
            "### TF-IDF score\n"
            "\n"
            "```text\n"
            "TF-IDF = TF × IDF\n"
            "       ≈ 0.167 × 0.301\n"
            "       ≈ 0.050\n"
            "```\n"
            "\n"
            "A higher value means the term is more distinctive for that document within the corpus.\n"
            "\n"
            "### What TF-IDF does well\n"
            "\n"
            "TF-IDF is useful when literal words matter:\n"
            "\n"
            "- product codes,\n"
            "- names,\n"
            "- error identifiers,\n"
            "- uncommon technical terms,\n"
            "- exact terminology.\n"
            "\n"
            "Its limitation is semantic generalization: `cars` and `vehicles` remain different features.\n"
            "\n"
            "---\n"
            "\n"

            "## 7. Cosine similarity\n"
            "\n"
            "Once text is represented as vectors, we need a way to compare them.\n"
            "\n"
            "Cosine similarity measures the **angle** between two vectors rather than their raw magnitude.\n"
            "\n"
            "A simplified formula is:\n"
            "\n"
            "```text\n"
            "cosine_similarity(A, B) = (A · B) / (||A|| ||B||)\n"
            "```\n"
            "\n"
            "The important intuition is:\n"
            "\n"
            "- same direction -> high similarity,\n"
            "- different direction -> lower similarity.\n"
            "\n"
            "For many text vectors, cosine similarity is useful because two documents can be treated "
            "as similar even when one is longer than the other.\n"
            "\n"
            "The chapter also uses cosine distance:\n"
            "\n"
            "```text\n"
            "cosine_distance = 1 - cosine_similarity\n"
            "```\n"
            "\n"
            "Therefore:\n"
            "\n"
            "- higher similarity means closer,\n"
            "- lower distance means closer.\n"
            "\n"
            "Do not accidentally rank cosine distance as though larger were better.\n"
            "\n"
            "[[IMAGE_NEEDED: Cosine similarity intuition | "
            "Draw two vector pairs from the same origin: one pair with a small angle labeled high "
            "similarity, and another with a large angle labeled low similarity | "
            "Learner should notice that cosine comparison focuses on direction rather than vector length]]\n"
            "\n"
            "---\n"
            "\n"

            "## 8. TF-IDF similarity in Python\n"
            "\n"
            "The chapter demonstrates the basic process with scikit-learn.\n"
            "\n"
            "```python\n"
            "from sklearn.feature_extraction.text import TfidfVectorizer\n"
            "from sklearn.metrics.pairwise import cosine_similarity\n"
            "\n"
            "documents = [\n"
            "    \"The sky is blue and beautiful.\",\n"
            "    \"Love this blue and beautiful sky!\",\n"
            "    \"The quick brown fox jumps over the lazy dog.\",\n"
            "]\n"
            "\n"
            "vectorizer = TfidfVectorizer()\n"
            "X = vectorizer.fit_transform(documents)\n"
            "\n"
            "similarities = cosine_similarity(X)\n"
            "print(similarities)\n"
            "```\n"
            "\n"
            "The result is a matrix. Entry `[i][j]` represents the similarity between document `i` "
            "and document `j`.\n"
            "\n"
            "Properties to notice:\n"
            "\n"
            "- diagonal entries are 1,\n"
            "- the matrix is symmetric,\n"
            "- sparse lexical overlap drives the result.\n"
            "\n"
            "---\n"
            "\n"

            "## 9. What a vector database does\n"
            "\n"
            "A vector database stores vectors together with the content and metadata they represent.\n"
            "\n"
            "A traditional lookup might ask:\n"
            "\n"
            "```text\n"
            "Find row WHERE user_id = 42\n"
            "```\n"
            "\n"
            "A vector search asks:\n"
            "\n"
            "```text\n"
            "Find the stored vectors most similar to this query vector.\n"
            "```\n"
            "\n"
            "A simple in-memory search looks like:\n"
            "\n"
            "```python\n"
            "def cosine_similarity_search(query, database, vectorizer, top_n=5):\n"
            "    query_vec = vectorizer.transform([query]).toarray()\n"
            "    similarities = cosine_similarity(query_vec, database)[0]\n"
            "    top_indices = similarities.argsort()[::-1][:top_n]\n"
            "    return [(idx, similarities[idx]) for idx in top_indices]\n"
            "```\n"
            "\n"
            "Production vector systems make this search efficient over much larger collections.\n"
            "\n"
            "---\n"
            "\n"

            "## 10. Neural embeddings: from words to meaning\n"
            "\n"
            "TF-IDF represents term importance. Neural embeddings attempt to represent semantic meaning.\n"
            "\n"
            "An embedding model maps text into a dense vector:\n"
            "\n"
            "```text\n"
            "\"cars need maintenance\"\n"
            "        |\n"
            "        v\n"
            "[0.12, -0.42, 0.08, ..., 0.31]\n"
            "```\n"
            "\n"
            "Semantically related pieces of text should end up relatively close in this learned vector space.\n"
            "\n"
            "### Sparse versus dense vectors\n"
            "\n"
            "TF-IDF vectors are usually sparse: most dimensions are zero.\n"
            "\n"
            "Neural embeddings are dense: information is distributed across many learned dimensions.\n"
            "\n"
            "### Interpretability trade-off\n"
            "\n"
            "A TF-IDF dimension can map to a known term. An individual neural-embedding dimension "
            "usually does not have a simple human-readable meaning.\n"
            "\n"
            "We interpret embeddings mainly through relationships such as similarity and distance.\n"
            "\n"
            "### Evaluate embeddings on your own domain\n"
            "\n"
            "The chapter uses an OpenAI embedding API as its practical example, but the broader lesson "
            "is to evaluate embedding quality on the actual content and queries your system will serve.\n"
            "\n"
            "---\n"
            "\n"

            "## 11. Visualizing high-dimensional embeddings\n"
            "\n"
            "Embedding vectors often have hundreds or thousands of dimensions, which humans cannot plot directly.\n"
            "\n"
            "The chapter demonstrates reducing them to three dimensions using PCA for visualization.\n"
            "\n"
            "```python\n"
            "import numpy as np\n"
            "from sklearn.decomposition import PCA\n"
            "\n"
            "embeddings_array = np.array(embeddings)\n"
            "\n"
            "pca = PCA(n_components=3)\n"
            "reduced = pca.fit_transform(embeddings_array)\n"
            "```\n"
            "\n"
            "The 3D coordinates are useful for **visualization**, not as a replacement for the original "
            "embedding space used for retrieval.\n"
            "\n"
            "[[IMAGE_NEEDED: Semantic embedding clusters in 3D | "
            "A 3D scatter plot with visually grouped clusters such as sky/blue sentences, dog/fox "
            "sentences, and breakfast/food sentences | "
            "Learner should notice that semantically related texts cluster near one another after dimensionality reduction]]\n"
            "\n"
            "---\n"
            "\n"

            "## 12. Querying embeddings with ChromaDB\n"
            "\n"
            "The chapter uses ChromaDB as a convenient local vector store for development.\n"
            "\n"
            "A simplified workflow is:\n"
            "\n"
            "```python\n"
            "import chromadb\n"
            "\n"
            "client = chromadb.Client()\n"
            "collection = client.create_collection(name=\"documents\")\n"
            "\n"
            "collection.add(\n"
            "    embeddings=embeddings,\n"
            "    documents=documents,\n"
            "    ids=ids,\n"
            ")\n"
            "\n"
            "results = collection.query(\n"
            "    query_embeddings=[query_embedding],\n"
            "    n_results=3,\n"
            ")\n"
            "```\n"
            "\n"
            "The chapter's example returns **distance** values, so lower values indicate closer matches.\n"
            "\n"
            "This is an easy place to introduce a retrieval bug: some systems return similarity, others return "
            "distance, and the ranking direction changes accordingly.\n"
            "\n"
            "{{exercise:M01.L06.EX01}}\n"
            "\n"
            "---\n"
            "\n"

            "## 13. Why vector search alone is not enough\n"
            "\n"
            "Semantic search is a strong foundation, but production RAG often needs more than one retrieval signal.\n"
            "\n"
            "The chapter identifies several common failure cases.\n"
            "\n"
            "| Problem | Example | Better supporting retrieval |\n"
            "|---|---|---|\n"
            "| Exact identifier missed | Error code `P0420` | Keyword or hybrid search |\n"
            "| Jargon mismatch | Different technical terms | Hybrid / synonym-aware lexical search |\n"
            "| Near duplicates dominate | Repeated product sheets | Deduplication / MMR / hybrid ranking |\n"
            "| Related but non-answering chunk | General page retrieved instead of exact fact | Reranking / filters |\n"
            "| Relationships required | \"Who reports to Alice's manager?\" | Graph or relational query |\n"
            "| Fresh structured fact needed | Current price | Relational/live data source |\n"
            "| Ambiguous word | `mouse` as animal vs device | Filters / hybrid search |\n"
            "| Restricted content | Unauthorized HR document | ACL-aware retrieval |\n"
            "\n"
            "The retrieval system's job is not merely to find related text. It must find the **right evidence**.\n"
            "\n"
            "---\n"
            "\n"

            "## 14. Choosing retrieval methods\n"
            "\n"
            "Different data types require different retrieval approaches.\n"
            "\n"
            "### Keyword / lexical search\n"
            "\n"
            "Best for:\n"
            "\n"
            "- exact terms,\n"
            "- IDs,\n"
            "- legal wording,\n"
            "- error codes,\n"
            "- rare domain vocabulary.\n"
            "\n"
            "### Vector search\n"
            "\n"
            "Best for:\n"
            "\n"
            "- paraphrases,\n"
            "- concept matching,\n"
            "- natural-language questions,\n"
            "- broad unstructured knowledge.\n"
            "\n"
            "### Hybrid search\n"
            "\n"
            "Combines lexical precision with semantic recall.\n"
            "\n"
            "### Relational database search\n"
            "\n"
            "Best for:\n"
            "\n"
            "- structured facts,\n"
            "- filters,\n"
            "- joins,\n"
            "- aggregations,\n"
            "- live canonical values.\n"
            "\n"
            "### Graph search\n"
            "\n"
            "Best for:\n"
            "\n"
            "- entity relationships,\n"
            "- hierarchy,\n"
            "- multihop questions,\n"
            "- explainable paths between facts.\n"
            "\n"
            "A capable RAG agent may have tools for several of these and choose the right one for the query.\n"
            "\n"
            "---\n"
            "\n"

            "## 15. Hybrid retrieval and Reciprocal Rank Fusion\n"
            "\n"
            "Hybrid retrieval usually runs at least two searches:\n"
            "\n"
            "```text\n"
            "User query\n"
            "   +--> lexical search -> ranked list A\n"
            "   +--> vector search  -> ranked list B\n"
            "                           |\n"
            "                           v\n"
            "                     fusion / reranking\n"
            "                           |\n"
            "                           v\n"
            "                     final context\n"
            "```\n"
            "\n"
            "The problem is that raw scores from different search systems may not be directly comparable.\n"
            "\n"
            "The chapter introduces **Reciprocal Rank Fusion (RRF)** as a common solution.\n"
            "\n"
            "A simplified RRF score is:\n"
            "\n"
            "```text\n"
            "RRF(document) = Σ 1 / (k + rank_i)\n"
            "```\n"
            "\n"
            "where `rank_i` is the document's position in each ranked list and `k` is a constant.\n"
            "\n"
            "The key idea is that RRF uses **rank positions**, not raw underlying similarity/BM25 scores.\n"
            "\n"
            "A document that ranks highly in multiple retrieval systems receives a strong fused ranking.\n"
            "\n"
            "[[IMAGE_NEEDED: Hybrid retrieval with Reciprocal Rank Fusion | "
            "Show keyword search producing ranked list A and vector search producing ranked list B, "
            "then an RRF fusion block merging them into one final ranked list | "
            "Learner should notice that fusion combines rank positions from different scoring systems]]\n"
            "\n"
            "---\n"
            "\n"

            "## 16. Building a vector-search RAG agent\n"
            "\n"
            "The chapter builds a movie-script agent to demonstrate a complete RAG workflow.\n"
            "\n"
            "The process is:\n"
            "\n"
            "1. Load the document.\n"
            "2. Split it into chunks.\n"
            "3. Store/index the chunks.\n"
            "4. Expose retrieval as an agent tool.\n"
            "5. Ask the agent to retrieve before answering.\n"
            "6. Ground the response in retrieved text.\n"
            "\n"
            "A simplified chunker from the chapter looks like:\n"
            "\n"
            "```python\n"
            "def simple_chunk(text, max_tokens=200):\n"
            "    tokenizer = tiktoken.get_encoding(\"cl100k_base\")\n"
            "    words, chunk, chunks = text.split(), [], []\n"
            "\n"
            "    for word in words:\n"
            "        candidate = \" \".join(chunk + [word])\n"
            "\n"
            "        if len(tokenizer.encode(candidate)) > max_tokens:\n"
            "            chunks.append(\" \".join(chunk))\n"
            "            chunk = [word]\n"
            "        else:\n"
            "            chunk.append(word)\n"
            "\n"
            "    if chunk:\n"
            "        chunks.append(\" \".join(chunk))\n"
            "\n"
            "    return chunks\n"
            "```\n"
            "\n"
            "Then retrieval becomes an agent tool:\n"
            "\n"
            "```python\n"
            "@function_tool\n"
            "def search_script(query: str, top_k: int = 3) -> str:\n"
            "    results = collection.query(\n"
            "        query_texts=[query],\n"
            "        n_results=top_k,\n"
            "    )\n"
            "\n"
            "    docs = results[\"documents\"][0]\n"
            "    return \"\\n\\n\".join(docs) if docs else \"No relevant documents found.\"\n"
            "```\n"
            "\n"
            "The LLM is not the database. It decides when and how to use the retrieval capability.\n"
            "\n"
            "---\n"
            "\n"

            "## 17. Grounding: make retrieved evidence authoritative\n"
            "\n"
            "Retrieval alone does not guarantee a grounded answer.\n"
            "\n"
            "The model may still rely on information encoded in its own parameters unless the system "
            "explicitly constrains how answers should be produced.\n"
            "\n"
            "A strong grounding instruction is similar to:\n"
            "\n"
            "```text\n"
            "Answer only using the retrieved context.\n"
            "If the retrieved context does not contain the answer, say so clearly.\n"
            "Cite the source passage supporting each factual claim.\n"
            "```\n"
            "\n"
            "### Weak grounding\n"
            "\n"
            "The answer generally follows retrieved content but may include outside knowledge.\n"
            "\n"
            "### Strong grounding\n"
            "\n"
            "Each claim can be traced to retrieved evidence, usually with citations.\n"
            "\n"
            "Strong grounding is especially important when incorrect answers have meaningful consequences.\n"
            "\n"
            "### Grounding is not only a prompt problem\n"
            "\n"
            "Grounding quality also depends on:\n"
            "\n"
            "- chunk quality,\n"
            "- retrieval relevance,\n"
            "- source quality,\n"
            "- citation handling,\n"
            "- evaluation.\n"
            "\n"
            "A perfect grounding prompt cannot repair consistently bad retrieval.\n"
            "\n"
            "---\n"
            "\n"

            "## 18. Building a hybrid RAG agent\n"
            "\n"
            "A hybrid agent can expose separate tools for lexical and semantic retrieval.\n"
            "\n"
            "Conceptually:\n"
            "\n"
            "```python\n"
            "agent = Agent(\n"
            "    name=\"Script Agent\",\n"
            "    instructions=\"\"\"\n"
            "Use semantic search for conceptual questions.\n"
            "Use keyword search for exact words, phrases, numbers, and identifiers.\n"
            "Use both when necessary.\n"
            "\n"
            "Answer only from retrieved script evidence.\n"
            "If evidence is missing, say so.\n"
            "Cite the retrieved references used for every answer.\n"
            "\"\"\",\n"
            "    tools=[\n"
            "        search_script_with_vector_similarity,\n"
            "        search_script_with_keyword,\n"
            "    ],\n"
            ")\n"
            "```\n"
            "\n"
            "The agent adds a reasoning layer on top of the retrieval tools: it can decide which search "
            "mode is appropriate, combine results, and answer only from supported evidence.\n"
            "\n"
            "{{exercise:M01.L06.EX02}}\n"
            "\n"
            "---\n"
            "\n"

            "## 19. Agent memory as architecture, not biology\n"
            "\n"
            "The chapter uses familiar labels such as short-term and long-term memory, but it warns "
            "against taking the human-memory analogy too literally.\n"
            "\n"
            "A clearer engineering model is:\n"
            "\n"
            "### Context window\n"
            "\n"
            "Information available inside the current model call.\n"
            "\n"
            "### External storage\n"
            "\n"
            "Databases, vector stores, files, or graphs that persist outside the model.\n"
            "\n"
            "### State management\n"
            "\n"
            "Working notes, scratchpads, task state, and plan trackers used during a workflow.\n"
            "\n"
            "### Retrieval\n"
            "\n"
            "Mechanisms that bring the right stored information back into the current context.\n"
            "\n"
            "This architecture is more useful than imagining that the agent 'remembers' in the same "
            "way a person does.\n"
            "\n"
            "---\n"
            "\n"

            "## 20. Working, semantic, episodic, procedural, and multimodal memory\n"
            "\n"
            "The chapter discusses several memory labels as useful shorthand.\n"
            "\n"
            "### Working / short-term memory\n"
            "\n"
            "Recent conversation and task context available during active work.\n"
            "\n"
            "### Long-term semantic memory\n"
            "\n"
            "Persisted facts and conceptual information retrieved later.\n\n{{image:semantic-memory-workflow}}\n"
            "\n"
            "### Episodic memory\n"
            "\n"
            "Stored events or experiences.\n"
            "\n"
            "Example:\n"
            "\n"
            "```text\n"
            "2026-10-02: User completed the onboarding workflow.\n"
            "```\n"
            "\n"
            "### Procedural memory\n"
            "\n"
            "Stored processes, steps, or repeated procedures.\n"
            "\n"
            "### Multimodal retrieval\n"
            "\n"
            "The chapter uses the term sensory memory for retrieving images, audio, or other modalities "
            "using embedding-and-search mechanics similar to text retrieval.\n\n{{image:memory-types}}\n"
            "\n"
            "The main engineering lesson is that the storage and retrieval method should match the information type.\n"
            "\n"
            "---\n"
            "\n"

            "## 21. Graph memory for entities and relationships\n"
            "\n"
            "Semantic vectors are good at fuzzy meaning. Graph databases are good at explicit relationships.\n"
            "\n"
            "Suppose we store:\n"
            "\n"
            "```text\n"
            "Michael --lives_in--> Calgary\n"
            "Michael --works_at--> Company A\n"
            "Company A --located_in--> Alberta\n"
            "```\n"
            "\n"
            "A graph can efficiently answer relationship-based questions by traversing edges.\n"
            "\n"
            "### Strengths\n"
            "\n"
            "- clear entities,\n"
            "- explicit relations,\n"
            "- multihop traversal,\n"
            "- inspectable paths.\n"
            "\n"
            "### Limitations\n"
            "\n"
            "- fuzzy language may not match exact entity names,\n"
            "- LLM-based fact extraction can create mistakes,\n"
            "- aliases such as `Doc` and `Doc Brown` may become separate nodes,\n"
            "- dense graphs create their own scaling and maintenance problems.\n"
            "\n"
            "This motivates **hybrid memory**.\n"
            "\n"
            '{{image:graph-memory}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 22. Adding memory through MCP\n"
            "\n"
            "The chapter demonstrates attaching a reference memory server through MCP.\n"
            "\n"
            "A simplified structure is:\n"
            "\n"
            "```python\n"
            "from agents import Agent\n"
            "from agents.mcp import MCPServerStdio\n"
            "\n"
            "memory_srv = MCPServerStdio(\n"
            "    name=\"memory\",\n"
            "    params={\n"
            "        \"command\": \"npx\",\n"
            "        \"args\": [\n"
            "            \"-y\",\n"
            "            \"@modelcontextprotocol/server-memory@latest\",\n"
            "        ],\n"
            "    },\n"
            ")\n"
            "\n"
            "agent = Agent(\n"
            "    name=\"Memory Agent\",\n"
            "    instructions=(\n"
            "        \"Track relevant facts and relationships, and retrieve them when useful.\"\n"
            "    ),\n"
            "    mcp_servers=[memory_srv],\n"
            ")\n"
            "```\n"
            "\n"
            "The MCP layer standardizes the interface. The real memory behavior still depends on:\n"
            "\n"
            "- what the agent chooses to store,\n"
            "- how facts are extracted,\n"
            "- what the backend persists,\n"
            "- how retrieval is performed,\n"
            "- access and privacy controls.\n"
            "\n"
            "---\n"
            "\n"

            "## 23. Hybrid memory: semantic context plus structured relationships\n"
            "\n"
            "The chapter combines semantic memory and graph memory.\n"
            "\n"
            "A representative workflow is:\n"
            "\n"
            "```text\n"
            "User input\n"
            "   |\n"
            "   v\n"
            "Semantic search\n"
            "   |\n"
            "   v\n"
            "Extract relevant entities / context\n"
            "   |\n"
            "   v\n"
            "Graph search\n"
            "   |\n"
            "   v\n"
            "Combine semantic context + graph facts\n"
            "   |\n"
            "   v\n"
            "Respond\n"
            "   |\n"
            "   v\n"
            "Capture useful new memory\n"
            "```\n"
            "\n"
            "The two stores solve different retrieval problems:\n"
            "\n"
            "- semantic store: fuzzy conversational meaning,\n"
            "- graph store: entities, relationships, and explicit facts.\n"
            "\n"
            "More advanced systems may add SQL, lexical search, or other stores when the use case requires them.\n"
            "\n"
            "---\n"
            "\n"

            "## 24. Learning examples versus production memory\n"
            "\n"
            "The chapter explicitly notes that simple local or in-memory examples are educational, not complete production systems.\n"
            "\n"
            "Production memory additionally needs:\n"
            "\n"
            "- persistent storage,\n"
            "- access control,\n"
            "- observability,\n"
            "- retrieval-quality evaluation,\n"
            "- policies for stale information,\n"
            "- correction and update mechanisms,\n"
            "- clear user/tenant separation,\n"
            "- privacy and retention rules.\n"
            "\n"
            "The MCP server is only the interface. The quality of memory comes from the entire pipeline behind it.\n"
            "\n"
            "---\n"
            "\n"

            "## 25. Semantic augmentation of memories\n"
            "\n"
            "A stored memory may be difficult to retrieve if future users phrase their questions differently.\n"
            "\n"
            "The chapter describes augmenting memories with additional semantic cues or likely retrieval questions.\n"
            "\n"
            "Example memory:\n"
            "\n"
            "```text\n"
            "User completed the onboarding flow on October 2.\n"
            "```\n"
            "\n"
            "Possible retrieval cues:\n"
            "\n"
            "```text\n"
            "When did the user finish onboarding?\n"
            "Has onboarding been completed?\n"
            "What happened during the October onboarding session?\n"
            "```\n"
            "\n"
            "These extra semantic representations can improve future retrieval because the stored item is "
            "connected to several ways the information may later be requested.\n"
            "\n"
            "---\n"
            "\n"

            "## 26. Memory and knowledge compression\n"
            "\n"
            "As stores grow, they may accumulate duplicates, repeated observations, and verbose histories.\n"
            "\n"
            "Compression reduces that clutter.\n"
            "\n"
            "The chapter describes a pattern such as:\n"
            "\n"
            "```text\n"
            "Many memory items\n"
            "      |\n"
            "      v\n"
            "Cluster similar items\n"
            "      |\n"
            "      v\n"
            "Summarize each cluster\n"
            "      |\n"
            "      v\n"
            "Store compact representations\n"
            "```\n"
            "\n"
            "Clustering methods such as k-means can group semantically related items before summarization.\n"
            "\n"
            "Compression may help when:\n"
            "\n"
            "- many memories are repetitive,\n"
            "- source material is verbose,\n"
            "- retrieval results are dominated by duplicates,\n"
            "- token cost from retrieved context is growing.\n"
            "\n"
            "But compression has a cost: summarization can remove details. Therefore the compression policy must "
            "match the application's need for fidelity.\n"
            "\n"
            '{{image:memory-compression}}'
            '\n'
            "\n"
            "---\n"
            "\n"

            "## 27. Forgetting and retention\n"
            "\n"
            "Sometimes summarization is not enough. Some information should eventually stop being retrieved.\n"
            "\n"
            "Forgetting may be useful when stored items are:\n"
            "\n"
            "- repetitive,\n"
            "- obsolete,\n"
            "- low-value,\n"
            "- contradicted by newer information,\n"
            "- no longer relevant to the agent's purpose.\n"
            "\n"
            "The chapter contrasts two ideas:\n"
            "\n"
            "- **Compression:** preserve the important information in a smaller representation.\n"
            "- **Forgetting:** remove information that should no longer participate in retrieval.\n"
            "\n"
            "Retention is also an operational and compliance concern. Aggressive deletion may be inappropriate "
            "when an application must retain records, while never removing anything can produce stale or noisy retrieval.\n"
            "\n"
            "The correct policy depends on the application.\n"
            "\n"
            "---\n"
            "\n"

            "## 28. Practical RAG and memory design playbook\n"
            "\n"
            "Use this sequence when designing an agent knowledge or memory system.\n"
            "\n"
            "### Step 1 — Identify the information type\n"
            "\n"
            "Is it free text, exact terminology, relational facts, live structured data, or past interaction?\n"
            "\n"
            "### Step 2 — Choose storage around retrieval needs\n"
            "\n"
            "Do not start with a vector database merely because RAG is popular.\n"
            "\n"
            "### Step 3 — Design ingestion and chunking\n"
            "\n"
            "Chunks should preserve enough context to answer likely queries.\n"
            "\n"
            "### Step 4 — Pick retrieval signals\n"
            "\n"
            "Use lexical, vector, SQL, graph, or hybrid retrieval according to the data.\n"
            "\n"
            "### Step 5 — Retrieve only enough context\n"
            "\n"
            "More chunks are not automatically better.\n"
            "\n"
            "### Step 6 — Ground the answer\n"
            "\n"
            "Make retrieved evidence authoritative and require citations when appropriate.\n"
            "\n"
            "### Step 7 — Evaluate retrieval separately from generation\n"
            "\n"
            "If the right evidence was never retrieved, prompt tuning alone cannot fix the answer.\n"
            "\n"
            "### Step 8 — Make memory selective\n"
            "\n"
            "Not every conversation detail deserves persistent storage.\n"
            "\n"
            "### Step 9 — Maintain the store\n"
            "\n"
            "Update, compress, deduplicate, or forget stale information.\n"
            "\n"
            "### Step 10 — Protect access\n"
            "\n"
            "Retrieval must respect user and tenant permissions before content reaches the model.\n"
            "\n"
            "---\n"
            "\n"

            "## Important misconceptions\n"
            "\n"
            "### Misconception 1: RAG means vector search\n"
            "\n"
            "> Vector search is one retrieval technique, not the whole RAG architecture.\n"
            "\n"
            "Production RAG may use lexical, relational, graph, or hybrid retrieval as well.\n"
            "\n"
            "### Misconception 2: Similar means correct\n"
            "\n"
            "> Semantic similarity measures related meaning, not truth or authority.\n"
            "\n"
            "Source quality and grounding still matter.\n"
            "\n"
            "### Misconception 3: Larger top-K always improves answers\n"
            "\n"
            "> More retrieved chunks can add noise, increase tokens, and dilute relevant evidence.\n"
            "\n"
            "K should be evaluated against actual queries.\n"
            "\n"
            "### Misconception 4: Embedding search replaces exact keyword search\n"
            "\n"
            "> Exact IDs, numbers, names, and wording often benefit from lexical retrieval.\n"
            "\n"
            "Hybrid systems combine both strengths.\n"
            "\n"
            "### Misconception 5: A grounded prompt fixes bad retrieval\n"
            "\n"
            "> The model cannot cite evidence that the retrieval layer never found.\n"
            "\n"
            "Retrieval and generation must be evaluated separately.\n"
            "\n"
            "### Misconception 6: Agent memory is like human memory\n"
            "\n"
            "> Agent memory is implemented through context, storage, state, and retrieval.\n"
            "\n"
            "Human cognitive labels are useful metaphors, not literal mechanisms.\n"
            "\n"
            "### Misconception 7: Store everything forever\n"
            "\n"
            "> Unlimited memory creates redundancy, stale facts, privacy risk, and retrieval noise.\n"
            "\n"
            "Memory needs maintenance and retention policies.\n"
            "\n"
            "---\n"
            "\n"

            "## Key terminology\n"
            "\n"
            "| Term | Meaning |\n"
            "|---|---|\n"
            "| Retrieval | Finding relevant information in an external store |\n"
            "| Augmentation | Adding retrieved information to the current model context |\n"
            "| RAG | Retrieval-augmented generation |\n"
            "| Chunk | A segment of source material indexed and retrieved as a unit |\n"
            "| Embedding | Dense numeric representation used for semantic comparison |\n"
            "| Vector database | Store optimized for similarity search over vectors |\n"
            "| TF-IDF | Lexical weighting method based on term frequency and corpus rarity |\n"
            "| Cosine similarity | Angular similarity between vectors |\n"
            "| Cosine distance | `1 - cosine similarity` |\n"
            "| Top-K | Number of highest-ranked retrieval results returned |\n"
            "| Semantic search | Retrieval by meaning rather than exact surface terms |\n"
            "| Keyword search | Retrieval using exact words, tokens, or lexical signals |\n"
            "| Hybrid search | Combination of semantic and lexical/other retrieval signals |\n"
            "| RRF | Reciprocal Rank Fusion, a rank-based result-merging method |\n"
            "| Grounding | Constraining generated claims to retrieved evidence |\n"
            "| Working memory | Current task/conversation state available during active work |\n"
            "| Long-term memory | Persisted information stored outside the current context |\n"
            "| Graph memory | Memory represented as entities, relations, and observations |\n"
            "| Episodic memory | Stored events or experiences |\n"
            "| Procedural memory | Stored processes or steps |\n"
            "| Compression | Consolidating related stored items into smaller representations |\n"
            "| Forgetting | Removing information from future retrieval according to policy |\n"
            "\n"
            "---\n"
            "\n"

            "## Self-check\n"
            "\n"
            "Before continuing, make sure you can answer:\n"
            "\n"
            "1. Why can external storage be much larger than an LLM context window?\n"
            "2. How is knowledge different from memory?\n"
            "3. What are retrieval and augmentation?\n"
            "4. What happens during RAG ingestion?\n"
            "5. What happens during RAG retrieval?\n"
            "6. Why are the embedding model and generative LLM separate components?\n"
            "7. What is TF-IDF good at, and what does it miss?\n"
            "8. What does cosine similarity measure?\n"
            "9. Why can vector similarity retrieve a related but incorrect result?\n"
            "10. Why can top-K cause retrieval misses?\n"
            "11. When should keyword search be preferred or added?\n"
            "12. Why does hybrid search improve coverage?\n"
            "13. What problem does RRF solve?\n"
            "14. What does grounding require beyond a prompt instruction?\n"
            "15. Why are graph databases useful for memory?\n"
            "16. What does MCP contribute to memory integration?\n"
            "17. Why might semantic and graph memory be combined?\n"
            "18. When is memory compression useful?\n"
            "19. How is forgetting different from compression?\n"
            "20. What additional controls does production memory require?\n"
            "\n"
            "---\n"
            "\n"

            "## Retain this idea\n"
            "\n"
            "**RAG and agent memory solve the same architectural problem: a model can only use a "
            "bounded amount of context at once, while useful knowledge and experience live in much "
            "larger external stores. Reliable agents therefore retrieve selectively, combine the "
            "right search methods, ground outputs in evidence, and maintain their memory stores so "
            "relevant information remains findable without letting stale or redundant context take over.**\n"
        ),

        "estimated_minutes": 255,

        "has_code_examples": True,

        "has_manual_image_requests": True,

        "sections": [
            {"id": "why-retrieval", "title": "Why agents need retrieval", "order": 1},
            {"id": "knowledge-vs-memory", "title": "Knowledge and memory are siblings, not twins", "order": 2},
            {"id": "retrieval-augmentation", "title": "Retrieval and augmentation", "order": 3},
            {"id": "rag-phases", "title": "The two phases of a RAG system", "order": 4},
            {"id": "semantic-search", "title": "Semantic search: retrieve by meaning", "order": 5},
            {"id": "tfidf", "title": "Start simple: TF-IDF", "order": 6},
            {"id": "cosine-similarity", "title": "Cosine similarity", "order": 7},
            {"id": "tfidf-code", "title": "TF-IDF similarity in Python", "order": 8},
            {"id": "vector-database", "title": "What a vector database does", "order": 9},
            {"id": "neural-embeddings", "title": "Neural embeddings: from words to meaning", "order": 10},
            {"id": "embedding-visualization", "title": "Visualizing high-dimensional embeddings", "order": 11},
            {"id": "chromadb", "title": "Querying embeddings with ChromaDB", "order": 12},
            {"id": "vector-limitations", "title": "Why vector search alone is not enough", "order": 13},
            {"id": "retrieval-methods", "title": "Choosing retrieval methods", "order": 14},
            {"id": "hybrid-search", "title": "Hybrid retrieval and Reciprocal Rank Fusion", "order": 15},
            {"id": "rag-agent", "title": "Building a vector-search RAG agent", "order": 16},
            {"id": "grounding", "title": "Grounding: make retrieved evidence authoritative", "order": 17},
            {"id": "hybrid-rag-agent", "title": "Building a hybrid RAG agent", "order": 18},
            {"id": "memory-architecture", "title": "Agent memory as architecture, not biology", "order": 19},
            {"id": "memory-types", "title": "Working, semantic, episodic, procedural, and multimodal memory", "order": 20},
            {"id": "graph-memory", "title": "Graph memory for entities and relationships", "order": 21},
            {"id": "mcp-memory", "title": "Adding memory through MCP", "order": 22},
            {"id": "hybrid-memory", "title": "Hybrid memory: semantic context plus structured relationships", "order": 23},
            {"id": "production-memory", "title": "Learning examples versus production memory", "order": 24},
            {"id": "memory-augmentation", "title": "Semantic augmentation of memories", "order": 25},
            {"id": "compression", "title": "Memory and knowledge compression", "order": 26},
            {"id": "forgetting", "title": "Forgetting and retention", "order": 27},
            {"id": "rag-playbook", "title": "Practical RAG and memory design playbook", "order": 28},
        ],
    },


    # =======================================================================
    # INLINE EXERCISES
    # =======================================================================

    "exercises": [
        {
            "id": "M01.L06.EX01",

            "title": "From Lexical Vectors to Semantic Retrieval",

            "lesson_code": "M01.L06",

            "section_id": "chromadb",

            "placement": "after_section",

            "description": (
                "Build the retrieval foundations step by step and compare what "
                "changes when lexical TF-IDF vectors are replaced by semantic embeddings."
            ),

            "instructions": (
                "Use a small corpus of 6-10 short sentences.\n"
                "1. Build TF-IDF vectors with `TfidfVectorizer`.\n"
                "2. Calculate the cosine-similarity matrix.\n"
                "3. Run at least two lexical queries and record the top three matches.\n"
                "4. Replace TF-IDF vectors with a semantic embedding helper available in your environment.\n"
                "5. Run the same queries and compare ranking changes.\n"
                "6. Store the semantic embeddings and documents in a ChromaDB collection.\n"
                "7. Query the collection and record IDs, documents, and distances.\n"
                "8. Explain why a smaller distance represents a closer match in the chapter's Chroma example.\n"
                "9. Identify one query where TF-IDF performs better because exact wording matters.\n"
                "10. Identify one query where semantic search performs better because meaning matters."
            ),

            "expected_output": (
                "A small working retrieval demo or carefully written implementation, "
                "two result comparisons, a ChromaDB query, and a short explanation of "
                "lexical versus semantic retrieval behavior."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "tf-idf",
                "cosine-similarity",
                "embeddings",
                "chromadb",
                "retrieval-evaluation",
            ],
        },

        {
            "id": "M01.L06.EX02",

            "title": "Design a Grounded Hybrid RAG and Memory Agent",

            "lesson_code": "M01.L06",

            "section_id": "hybrid-rag-agent",

            "placement": "after_section",

            "description": (
                "Combine retrieval methods, grounding, agent memory, and maintenance "
                "into one practical architecture."
            ),

            "instructions": (
                "Scenario: Build an internal company assistant that must answer policy questions "
                "and remember selected user preferences across sessions.\n"
                "1. Use semantic vector search for conceptual policy questions.\n"
                "2. Add keyword search for exact policy codes, dates, and phrases.\n"
                "3. Add a relational query tool for live structured values such as current limits.\n"
                "4. Define how keyword and vector results will be fused or jointly evaluated.\n"
                "5. Require strong grounding: every factual policy claim must cite retrieved evidence.\n"
                "6. Define the fallback response when retrieved context does not support an answer.\n"
                "7. Store conversational preference memories in a semantic memory store.\n"
                "8. Store explicit entities/relationships in a graph memory store only when useful.\n"
                "9. Define one access-control rule that must run before retrieval results reach the LLM.\n"
                "10. Define a maintenance policy for deduplication, compression, stale facts, and forgetting.\n"
                "11. Identify what you would trace and evaluate separately for retrieval and generation.\n"
                "12. Draw the complete flow from query -> retrieval tools -> fusion -> grounded answer -> memory update."
            ),

            "expected_output": (
                "A hybrid knowledge-and-memory architecture with at least three retrieval "
                "mechanisms, a grounding policy, evidence citations, memory rules, access "
                "control, maintenance policy, and observability plan."
            ),

            "difficulty": DifficultyLevel.beginner,

            "skill_tested": [
                "hybrid-rag",
                "grounding",
                "keyword-search",
                "vector-search",
                "sql-retrieval",
                "agent-memory",
                "graph-memory",
                "access-control",
                "memory-maintenance",
            ],
        },
    ],


    # =======================================================================
    # LESSON QUIZ
    # =======================================================================

    "quiz": {
        "id": "M01.L06.QZ01",

        "title": "Working with Memory and Knowledge RAG for Agents — Knowledge Check",

        "lesson_code": "M01.L06",

        "placement": "lesson_end",

        "questions": [
            {
                "id": "M01.L06.Q01",
                "section_id": "knowledge-vs-memory",
                "question": "Which example is best classified as agent memory?",
                "options": [
                    "A product manual indexed from a PDF",
                    "A user's preference captured from a previous conversation",
                    "A public standards document",
                    "A source-code repository",
                ],
                "correct": 1,
                "explanation": (
                    "Memory is interaction- or experience-derived information. The other "
                    "examples are external knowledge sources."
                ),
            },

            {
                "id": "M01.L06.Q02",
                "section_id": "rag-phases",
                "question": "Which operation belongs to RAG ingestion rather than query-time retrieval?",
                "options": [
                    "Embedding document chunks and storing them",
                    "Embedding the user's new query",
                    "Selecting top-K query results",
                    "Generating the final answer",
                ],
                "correct": 0,
                "explanation": (
                    "Ingestion prepares and indexes source material before user queries are answered."
                ),
            },

            {
                "id": "M01.L06.Q03",
                "section_id": "semantic-search",
                "question": "What does semantic search primarily optimize for?",
                "options": [
                    "Exact character matching",
                    "Meaning similarity",
                    "Database transaction ordering",
                    "File compression",
                ],
                "correct": 1,
                "explanation": (
                    "Semantic embeddings are designed so related meanings are represented nearby."
                ),
            },

            {
                "id": "M01.L06.Q04",
                "section_id": "tfidf",
                "question": "Why can TF-IDF be useful even when semantic embeddings are available?",
                "options": [
                    "It understands all synonyms automatically",
                    "It is strong for exact, rare, and interpretable lexical terms",
                    "It always produces dense vectors",
                    "It eliminates the need for ranking",
                ],
                "correct": 1,
                "explanation": (
                    "TF-IDF is predictable and effective when literal vocabulary, identifiers, "
                    "or rare terms matter."
                ),
            },

            {
                "id": "M01.L06.Q05",
                "section_id": "cosine-similarity",
                "question": "If cosine distance is used for ranking, which result is usually closer?",
                "options": [
                    "Distance 0.12",
                    "Distance 0.91",
                    "Distance 1.40",
                    "The largest distance",
                ],
                "correct": 0,
                "explanation": (
                    "Cosine distance is `1 - similarity`, so smaller values indicate closer vectors."
                ),
            },

            {
                "id": "M01.L06.Q06",
                "section_id": "vector-limitations",
                "question": "A query asks for exact error code P0420. Which retrieval addition is especially useful?",
                "options": [
                    "Only increase vector top-K indefinitely",
                    "Keyword or hybrid retrieval",
                    "Remove all metadata",
                    "Use graph traversal only",
                ],
                "correct": 1,
                "explanation": (
                    "Exact codes are lexical signals that semantic retrieval can miss."
                ),
            },

            {
                "id": "M01.L06.Q07",
                "section_id": "hybrid-search",
                "question": "What is a major reason RRF is useful for hybrid search?",
                "options": [
                    "It requires all search systems to use identical raw score scales",
                    "It combines ranked lists without depending on comparable raw scores",
                    "It removes the need for retrieval",
                    "It converts SQL rows into embeddings",
                ],
                "correct": 1,
                "explanation": (
                    "RRF uses rank position, making it robust when lexical and vector scores "
                    "have different meanings and scales."
                ),
            },

            {
                "id": "M01.L06.Q08",
                "section_id": "grounding",
                "question": "What is the strongest description of grounding?",
                "options": [
                    "Let the model answer from any source as long as it sounds plausible",
                    "Ensure answer claims can be traced to retrieved evidence",
                    "Always retrieve exactly ten chunks",
                    "Use only semantic embeddings",
                ],
                "correct": 1,
                "explanation": (
                    "Strong grounding ties claims to authoritative retrieved context, commonly "
                    "with explicit citations."
                ),
            },

            {
                "id": "M01.L06.Q09",
                "section_id": "memory-architecture",
                "question": "What is the most useful architectural distinction in agent memory?",
                "options": [
                    "Human memory versus computer memory",
                    "What fits in the current context versus what persists in external storage",
                    "Blue vectors versus red vectors",
                    "Prompts versus Python syntax",
                ],
                "correct": 1,
                "explanation": (
                    "The chapter emphasizes context-window state versus persistent external storage "
                    "as the meaningful engineering distinction."
                ),
            },

            {
                "id": "M01.L06.Q10",
                "section_id": "graph-memory",
                "question": "Which query is especially suitable for graph retrieval?",
                "options": [
                    "Find text semantically similar to 'cheap vehicle'",
                    "Who reports to Alice's manager?",
                    "Return documents containing exact code X17",
                    "Summarize a paragraph",
                ],
                "correct": 1,
                "explanation": (
                    "The query requires relationship traversal across connected entities."
                ),
            },

            {
                "id": "M01.L06.Q11",
                "section_id": "hybrid-memory",
                "question": "Why combine semantic memory with graph memory?",
                "options": [
                    "Because both stores solve exactly the same retrieval problem",
                    "To combine fuzzy contextual recall with structured entity relationships",
                    "To prevent any memory from being persistent",
                    "To remove the need for access control",
                ],
                "correct": 1,
                "explanation": (
                    "Semantic memory and graph memory provide complementary retrieval strengths."
                ),
            },

            {
                "id": "M01.L06.Q12",
                "section_id": "compression",
                "question": "When is memory compression especially useful?",
                "options": [
                    "When a store contains many repetitive or highly similar items",
                    "When every stored item is unique and must remain verbatim",
                    "When the system has no memory",
                    "Only before the first document is indexed",
                ],
                "correct": 0,
                "explanation": (
                    "Compression consolidates redundant groups into more compact representations."
                ),
            },

            {
                "id": "M01.L06.Q13",
                "section_id": "forgetting",
                "question": "How does forgetting differ from compression?",
                "options": [
                    "Forgetting removes information from future retrieval; compression tries to preserve important information more compactly",
                    "They are identical",
                    "Compression always deletes every source item",
                    "Forgetting increases vector dimensionality",
                ],
                "correct": 0,
                "explanation": (
                    "Compression consolidates; forgetting intentionally removes or expires information."
                ),
            },

            {
                "id": "M01.L06.Q14",
                "section_id": "rag-playbook",
                "type": "open",
                "question": (
                    "Design a knowledge-and-memory architecture for an internal engineering agent. "
                    "Explain how documents are ingested, which retrieval methods are used, how results "
                    "are fused, how answers are grounded, what memories are stored, how permissions "
                    "are enforced, and how stale or duplicate memories are maintained over time."
                ),
            },
        ],

        "passing_score": 70,
    },
}
