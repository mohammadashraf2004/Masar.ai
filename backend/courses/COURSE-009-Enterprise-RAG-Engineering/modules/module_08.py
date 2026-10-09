"""M01.L08 — Multimodal RAG.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Supplied source, Chapter 8, pages not provided.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L08"
MODULE_ORDER = 1
MODULE_TITLE = 'RAG Foundations'
MODULE_DESCRIPTION = 'Build, evaluate, operate, and extend RAG systems across text, tables, images, audio, video, and multimodal generation while preserving evidence and provenance.'
SOURCE_CHAPTER = 8
SOURCE_PAGES = "Not provided in supplied source"

TOPIC = {'title': 'Multimodal RAG',
 'slug': 'rag-foundations-m01-l08',
 'description': 'A study-ready guide to table-aware RAG, image retrieval and summarization, shared '
                'multimodal embeddings, audio/video ingestion, multimodal security, citations, '
                'observability, and evaluation.',
 'order': 8,
 'difficulty': 'intermediate',
 'estimated_hours': 11.5,
 'skill_tags': ['rag',
                'multimodal-rag',
                'tables',
                'docling',
                'vision-language-models',
                'multimodal-embeddings',
                'siglip',
                'audio-rag',
                'video-rag',
                'asr',
                'diarization',
                'visual-citations',
                'multimodal-evaluation',
                'security',
                'observability',
                'module-01'],
 'prerequisite_ids': ['M01.L01', 'M01.L02', 'M01.L03', 'M01.L04', 'M01.L05', 'M01.L06', 'M01.L07'],
 'lesson': {'title': 'Multimodal RAG',
            'content': '# Multimodal RAG\n'
                       '\n'
                       '> **Course:** Retrieval-Augmented Generation (RAG)  \n'
                       '> **Lesson:** M01.L08  \n'
                       '> **Module:** RAG Foundations  \n'
                       '> **Source alignment:** Supplied source, Chapter 8. Page numbers were not '
                       'provided. This lesson is an instructor-authored study adaptation rather '
                       'than a reproduction of the source text.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Learning outcomes\n'
                       '\n'
                       'By the end of this lesson, you should be able to:\n'
                       '\n'
                       '- Explain why enterprise RAG must support tables, images, audio, and '
                       'video.\n'
                       '- Compare conversion-based and native multimodal architectures.\n'
                       '- Build table-aware ingestion that preserves headers, units, rows, and '
                       'multi-page continuity.\n'
                       '- Explain the summary-pointer pattern for structured tables.\n'
                       '- Compare image summarization, raw-image generation, and shared multimodal '
                       'embeddings.\n'
                       '- Explain contrastive text–image retrieval and its limitations for '
                       'information-dense visuals.\n'
                       '- Design ASR pipelines with diarization, timestamps, and transcript '
                       'chunking.\n'
                       '- Choose among fixed-frame, temporal-segment, and keyframe video '
                       'strategies.\n'
                       '- Design visual citations and jump-to-source interfaces.\n'
                       '- Identify multimodal privacy, prompt-injection, and provenance risks.\n'
                       '- Evaluate retrieval and generation across multiple modalities.\n'
                       '- Design an observable production multimodal RAG architecture.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 1. Why Multimodal RAG Matters\n'
                       '\n'
                       'Text-only RAG works well only when the facts needed to answer a question '
                       'are actually represented in text. Enterprise knowledge is not that tidy. A '
                       'financial report may explain strategy in prose while placing the exact '
                       'numbers in a table. A maintenance manual may describe a procedure but show '
                       'the critical control position only in a diagram. A customer-service '
                       'recording may contain the words of a conversation, but tone, speaker '
                       'identity, and timing may change what those words mean.\n'
                       '\n'
                       'That creates a simple but important failure mode: a text-only system can '
                       'retrieve the correct document and still fail because the decisive evidence '
                       'lives in another modality. Multimodal RAG extends the grounding layer so '
                       'tables, images, audio, and video can become searchable evidence rather '
                       'than invisible attachments.\n'
                       '\n'
                       'The important mental model is that multimodal RAG is not a separate '
                       'species of RAG. The same broad stages still exist—ingestion, '
                       'representation, retrieval, and generation—but each modality needs its own '
                       'extraction, representation, and validation strategy.\n'
                       '\n'
                       '## 2. Conversion Versus Native Multimodal RAG\n'
                       '\n'
                       'The chapter distinguishes two broad production strategies.\n'
                       '\n'
                       '**Conversion** transforms non-text information into a text-friendly '
                       'representation. Tables can become JSON or dataframes, images can become '
                       'detailed captions, and audio can become diarized transcripts. The '
                       'converted representation then flows through a conventional text RAG stack. '
                       'This approach is attractive because it reuses mature text retrieval, '
                       'hybrid search, reranking, prompt engineering, and observability '
                       'infrastructure.\n'
                       '\n'
                       '**Native multimodal processing** keeps multiple modalities closer to their '
                       'original form. A multimodal embedding model may place text and images in a '
                       'shared vector space, while a vision-language model can inspect raw images '
                       'during answer generation. Native processing can preserve more visual '
                       'detail, but it often increases cost, latency, storage complexity, and '
                       'evaluation difficulty.\n'
                       '\n'
                       'A good production design does not choose based on fashion. It asks where '
                       'information loss is acceptable, where high fidelity is essential, and '
                       'whether the extra multimodal cost belongs at ingestion time or query '
                       'time.\n'
                       '\n'
                       '{{exercise:M01.L08.EX01}}\n'
                       '\n'
                       '[[IMAGE_NEEDED: Conversion vs native multimodal RAG | Side-by-side '
                       'architecture showing non-text data converted to text/JSON versus raw '
                       'multimodal embeddings/VLM path | Notice where information is transformed '
                       'and where expensive multimodal reasoning occurs]]\n'
                       '\n'
                       '## 3. Design Principle: Preserve Semantics, Not Just Bytes\n'
                       '\n'
                       'The goal of multimodal ingestion is not merely to extract *something* from '
                       'a file. It is to preserve the relationships that give the information '
                       'meaning.\n'
                       '\n'
                       'For a table, a number is meaningful because it belongs to a row and '
                       'column. For a chart, a bar height matters because of its axis and legend. '
                       'For audio, an utterance may matter because of who said it and when. For '
                       'video, an instruction may only make sense together with the object being '
                       'pointed at.\n'
                       '\n'
                       'This leads to a recurring design rule throughout the chapter: represent '
                       'each modality in a way that preserves the structure needed to answer '
                       'downstream questions. A parser that extracts every character but destroys '
                       'those relationships may be technically successful and still be useless for '
                       'RAG.\n'
                       '\n'
                       '## 4. Tables as Semantic Micro-Documents\n'
                       '\n'
                       'Tables are common in financial filings, scientific papers, product '
                       'manuals, insurance documents, healthcare records, and manufacturing '
                       'systems. They often contain high-density facts that are more authoritative '
                       'than the surrounding prose.\n'
                       '\n'
                       'A table should therefore be treated as a semantic unit rather than as '
                       'incidental formatting. The title, headers, row labels, units, footnotes, '
                       'and cell relationships all contribute meaning. In a bill of materials, for '
                       'example, quantity without the associated component identifier is not '
                       'useful. In a financial table, a value without its fiscal-year column can '
                       'be actively misleading.\n'
                       '\n'
                       'This is why table handling deserves a dedicated ingestion path rather than '
                       'being delegated blindly to a generic text extractor.\n'
                       '\n'
                       '## 5. The Three Stages of Table Extraction\n'
                       '\n'
                       'A robust table pipeline usually performs three logically separate '
                       'operations.\n'
                       '\n'
                       'First comes **table detection and structure recovery**. The parser must '
                       'locate the table within the page and infer rows, columns, merged cells, '
                       'and spanning headers—even when grid lines are missing or the table is '
                       'rotated.\n'
                       '\n'
                       'Second comes **OCR and semantic interpretation**. Characters are extracted '
                       'cell by cell rather than in ordinary reading order. The system must '
                       'distinguish headers from data and preserve the association between values '
                       'and their logical fields.\n'
                       '\n'
                       'Third comes **normalization**. Formatting noise is converted into a '
                       'consistent representation. Currency symbols, thousands separators, '
                       'parenthesized negative values, percentages, dates, and blank cells may '
                       'need normalization while retaining their semantic type.\n'
                       '\n'
                       'Separating these stages makes debugging easier. If a number is wrong, you '
                       'can ask whether the grid was detected incorrectly, OCR read the cell '
                       'incorrectly, or normalization transformed the value incorrectly.\n'
                       '\n'
                       '{{exercise:M01.L08.EX02}}\n'
                       '\n'
                       '[[IMAGE_NEEDED: Table extraction pipeline | Document page -> table '
                       'detection/grid recovery -> cell OCR/semantic roles -> normalized '
                       'dataframe/JSON | Notice that structure must be recovered before values are '
                       'interpreted]]\n'
                       '\n'
                       '## 6. Choosing Table Extraction Tools\n'
                       '\n'
                       'The source separates managed services from local/open-source tooling.\n'
                       '\n'
                       'Managed document services are useful when OCR quality is critical, '
                       'especially for scans, handwriting, and visually difficult forms. They '
                       'reduce infrastructure work but introduce API cost, network latency, vendor '
                       'dependencies, and possible constraints for private or air-gapped data.\n'
                       '\n'
                       'Local tools such as document parsers and table-focused libraries can be '
                       'attractive for digitally generated PDFs, high-volume ingestion, or '
                       'isolated environments. They also give engineering teams more control over '
                       'deployment and debugging.\n'
                       '\n'
                       'The most important production lesson is not the name of a specific parser. '
                       'It is that parser quality is data-dependent. Evaluate candidate tools on a '
                       'representative corpus instead of assuming one parser will work equally '
                       'well on all layouts.\n'
                       '\n'
                       '## 7. Table Extraction with Docling: What the Example Teaches\n'
                       '\n'
                       'The chapter uses Docling to demonstrate parsing a PDF into a structured '
                       'document object and exporting detected tables as dataframes. The important '
                       'lesson is not the exact API call; it is the intermediate representation.\n'
                       '\n'
                       'Once a table becomes a dataframe, you can inspect shape, column labels, '
                       'missing values, and row-level structure programmatically. That gives you a '
                       'validation surface before the data is embedded.\n'
                       '\n'
                       'A simplified pattern looks like this:\n'
                       '\n'
                       '```python\n'
                       'from docling.document_converter import DocumentConverter\n'
                       '\n'
                       'result = DocumentConverter().convert("report.pdf")\n'
                       'doc = result.document\n'
                       '\n'
                       'for table in doc.tables:\n'
                       '    df = table.export_to_dataframe()\n'
                       '    print(df.shape)\n'
                       '    print(df.head())\n'
                       '```\n'
                       '\n'
                       'In production, add quality checks before accepting a dataframe: reject '
                       'empty tables, detect suspiciously small column counts, verify important '
                       'headers, and log page provenance.\n'
                       '\n'
                       '## 8. Parser Failure Is Normal—Design for It\n'
                       '\n'
                       'The chapter intentionally shows a case where a parser returns an empty '
                       'table. That example matters because it breaks a dangerous assumption: '
                       'document parsing is not deterministic truth extraction.\n'
                       '\n'
                       'Layout complexity, borderless tables, merged cells, unusual rotations, '
                       'scanned pages, and weak OCR can all produce malformed results. Therefore, '
                       'parser output should be treated as a *candidate representation* that must '
                       'be validated.\n'
                       '\n'
                       'A useful production pattern is to maintain a small evaluation harness of '
                       'manually checked documents. Run candidate parsers against that set, score '
                       'structural correctness, and choose the best tool—or routing rule—for each '
                       'document class.\n'
                       '\n'
                       '{{exercise:M01.L08.EX03}}\n'
                       '\n'
                       '## 9. Conditional Parsing Pipelines\n'
                       '\n'
                       'At scale, one parser may be best for native PDFs, another for scans, and '
                       'another for tables with complex merged headers. That motivates conditional '
                       'routing.\n'
                       '\n'
                       'A triage stage can inspect file type, presence of selectable text, page '
                       'dimensions, OCR confidence, or known source system. It then dispatches the '
                       'document to an appropriate extraction path.\n'
                       '\n'
                       'This is the multimodal equivalent of model routing: use the expensive '
                       'capability only where it adds value. Conditional routing improves both '
                       'accuracy and cost efficiency while preserving a common downstream schema.\n'
                       '\n'
                       '## 10. Why Naive Chunking Breaks Tables\n'
                       '\n'
                       'Turning a table into Markdown and sending it through an ordinary character '
                       'splitter seems convenient, but it can destroy the very structure that '
                       'makes the table useful.\n'
                       '\n'
                       'The source demonstrates a common failure: the header lands in one chunk '
                       'while data rows land in later chunks. Retrieval may correctly find a row '
                       'containing the requested product, yet the generator sees numbers without '
                       'knowing which number is price, rating, or another field.\n'
                       '\n'
                       'The problem is not retrieval similarity. The problem is *semantic '
                       'amputation*: chunk boundaries have removed the schema.\n'
                       '\n'
                       'This illustrates a broader RAG lesson: chunking strategy must match data '
                       'structure. A good chunk for prose is not necessarily a good chunk for a '
                       'table.\n'
                       '\n'
                       '{{exercise:M01.L08.EX04}}\n'
                       '\n'
                       '## 11. Represent Tables as Structured Context\n'
                       '\n'
                       'A safer strategy is to preserve a table as structured data such as JSON '
                       'records or a dataframe. Each value remains associated with its column name '
                       'and row identity.\n'
                       '\n'
                       'For example:\n'
                       '\n'
                       '```python\n'
                       'records = [\n'
                       '    {"product": "Model-A", "price_usd": 299, "rating": 4.5},\n'
                       '    {"product": "Model-X", "price_usd": 899, "rating": 4.8},\n'
                       ']\n'
                       '```\n'
                       '\n'
                       'Modern LLMs are generally comfortable reasoning over JSON-like structures '
                       'because they have seen large amounts of code and structured text during '
                       'training.\n'
                       '\n'
                       'The crucial point is that retrieval and generation do not have to use the '
                       'same representation. You can retrieve via a compact textual summary but '
                       'generate using the full structured object.\n'
                       '\n'
                       '## 12. The Summary-Pointer Pattern for Tables\n'
                       '\n'
                       'Large tables create a retrieval problem: embedding the entire table may be '
                       'inefficient, while embedding individual rows may lose table-level '
                       'context.\n'
                       '\n'
                       'The chapter recommends a useful indirection pattern. Create a textual '
                       'summary of the table and embed that summary as the searchable chunk. Store '
                       'metadata that points back to the complete table.\n'
                       '\n'
                       'At query time:\n'
                       '\n'
                       '1. Retrieve the table summary.\n'
                       '2. Follow its pointer to the original dataframe or JSON object.\n'
                       '3. Insert the complete relevant structure into the generation context.\n'
                       '\n'
                       'This is a powerful RAG design pattern beyond tables. Retrieval can operate '
                       'on a compact *representation*, while generation can operate on the richer '
                       '*source object*.\n'
                       '\n'
                       '{{exercise:M01.L08.EX05}}\n'
                       '\n'
                       '## 13. Prompting with Mixed Text and Structured Data\n'
                       '\n'
                       'A multimodal or structured RAG prompt may contain ordinary text facts '
                       'alongside JSON or dataframe content. The formatting layer should identify '
                       'the type of each retrieved item and serialize it appropriately.\n'
                       '\n'
                       'A robust formatter can enforce row limits, preserve column names, and add '
                       'explicit truncation notes. That prevents an accidental giant table from '
                       'consuming the full context window.\n'
                       '\n'
                       'The generator should also be told how to treat the structured data: use it '
                       'as evidence, preserve units, avoid inventing missing cells, and state when '
                       'the requested value is unavailable.\n'
                       '\n'
                       'For smaller or older language models, examples of how to read nested JSON '
                       'may improve reliability.\n'
                       '\n'
                       '## 14. Why Multi-Page Tables Are a Special Case\n'
                       '\n'
                       'A logical table may span several physical pages. Many parsers return each '
                       'page fragment as a separate table, which creates two failure modes.\n'
                       '\n'
                       'If headers repeat on every page, concatenating fragments naively produces '
                       'duplicate header rows. If headers do not repeat, later fragments become '
                       'headless and lose their schema.\n'
                       '\n'
                       'A post-processing layer should detect likely continuation fragments using '
                       'page adjacency, column count, column types, repeated headers, and other '
                       'structural signals. Once continuity is established, fragments can be '
                       'stitched into one master structure before summarization and indexing.\n'
                       '\n'
                       '{{exercise:M01.L08.EX06}}\n'
                       '\n'
                       '## 15. A Practical Table-Stitching Heuristic\n'
                       '\n'
                       'The source demonstrates stitching adjacent table fragments when they have '
                       'compatible shapes.\n'
                       '\n'
                       'A simplified version is:\n'
                       '\n'
                       '```python\n'
                       'def stitch(current, next_df):\n'
                       '    if list(current.columns) == list(next_df.columns):\n'
                       '        return pd.concat([current, next_df], ignore_index=True)\n'
                       '    return None\n'
                       '```\n'
                       '\n'
                       'Real systems need stronger checks. Matching column count alone can create '
                       'false merges when unrelated tables happen to have the same width. Better '
                       'signals include page location, table title, data types, header similarity, '
                       'and continuation markers.\n'
                       '\n'
                       'The purpose of stitching is not merely to make a larger dataframe. It '
                       'restores the logical object that existed before pagination broke it '
                       'apart.\n'
                       '\n'
                       '## 16. End-to-End Table RAG Flow\n'
                       '\n'
                       'A table-aware ingestion path can be summarized as:\n'
                       '\n'
                       '**detect → extract structure → OCR/interpret → normalize → validate → '
                       'summarize → embed summary → store full table + pointer**\n'
                       '\n'
                       'The query path becomes:\n'
                       '\n'
                       '**query → retrieve summary → dereference table → provide structured '
                       'context → generate answer**\n'
                       '\n'
                       'Notice that the vector index never has to contain every raw cell as one '
                       'giant embedding. The index contains a retrieval-friendly representation '
                       'while the authoritative structured object remains available for generation '
                       'and citation.\n'
                       '\n'
                       'This separation improves both search quality and fidelity.\n'
                       '\n'
                       '{{image:table-rag-flow}}'
                       '\n'
                       '\n'
                       '## 17. Why Images Need More Than OCR\n'
                       '\n'
                       'OCR can recover visible text from an image, but many images encode meaning '
                       'spatially rather than textually.\n'
                       '\n'
                       'A flowchart communicates relationships through arrows. A bar chart encodes '
                       'magnitude through height. A pie chart encodes proportions through area. A '
                       'technical diagram may show which component connects to which subsystem.\n'
                       '\n'
                       'A text-only parser may extract labels while losing the relationships among '
                       'them. Therefore, image understanding needs a semantic representation, not '
                       'just character extraction.\n'
                       '\n'
                       '## 18. Two Main Image Strategies\n'
                       '\n'
                       'The chapter presents two major strategies for visual information.\n'
                       '\n'
                       '**Image summarization** uses a vision-language model during ingestion to '
                       'produce a detailed text description. Retrieval remains text-based.\n'
                       '\n'
                       '**Multimodal retrieval** represents images directly, often through a '
                       'multimodal embedding model, and can send the original image to a '
                       'vision-language model at query time.\n'
                       '\n'
                       'Summarization spends intelligence earlier, at ingestion, and makes query '
                       'serving cheaper. Native retrieval preserves more visual fidelity but often '
                       'spends more intelligence later, at query time.\n'
                       '\n'
                       'The decision is fundamentally about where you want to pay the cost and how '
                       'much detail you can afford to compress.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Image summarization vs multimodal retrieval | '
                       'Caption-based text retrieval path beside raw-image/shared-embedding path | '
                       'Compare ingestion cost, query cost, and retained visual detail]]\n'
                       '\n'
                       '## 19. Image Summarization During Ingestion\n'
                       '\n'
                       'A useful image-summary prompt should ask for more than a generic caption. '
                       'It should capture the main subject, text visible in the image, graph '
                       'trends, axes and legends, diagram relationships, and any detail likely to '
                       'support future questions.\n'
                       '\n'
                       'The summary becomes a searchable chunk, while the original image is stored '
                       'separately. Metadata links the chunk to the original image and its '
                       'document/page provenance.\n'
                       '\n'
                       'This approach integrates smoothly with standard semantic search, BM25, '
                       'reranking, and text-only generation because the visual information has '
                       'been translated into language.\n'
                       '\n'
                       '{{exercise:M01.L08.EX07}}\n'
                       '\n'
                       '## 20. The Information Bottleneck of Image Summaries\n'
                       '\n'
                       'An image summary is a lossy compression.\n'
                       '\n'
                       'If the captioning model overlooks a small but important value, later '
                       'queries cannot recover it from the summary alone. This is the central '
                       'limitation of conversion-based multimodal RAG.\n'
                       '\n'
                       'A useful mitigation is a two-tier design: retrieve using the summary, '
                       'then—when the generation model supports vision—load the original image and '
                       'let the model inspect it again.\n'
                       '\n'
                       'That separates *searchability* from *final-fidelity reasoning*.\n'
                       '\n'
                       '## 21. Retrieve by Summary, Reason over the Original Image\n'
                       '\n'
                       'The chapter demonstrates a pattern in which image summaries are embedded '
                       'in the vector store, but the original image bytes are stored in a document '
                       'store.\n'
                       '\n'
                       'When a summary matches a query, the system follows a document identifier '
                       'back to the raw image. The generator receives both textual context and the '
                       'image.\n'
                       '\n'
                       'Conceptually:\n'
                       '\n'
                       '```python\n'
                       'summary_hits = vectorstore.similarity_search(query, k=5)\n'
                       'image_ids = [hit.metadata["image_id"] for hit in summary_hits]\n'
                       'images = image_store.get_many(image_ids)\n'
                       '\n'
                       'answer = vision_model.generate(query=query, images=images, '
                       'text_context=summary_hits)\n'
                       '```\n'
                       '\n'
                       'This pattern preserves efficient retrieval while allowing high-fidelity '
                       'visual reasoning at the final step.\n'
                       '\n'
                       '{{exercise:M01.L08.EX08}}\n'
                       '\n'
                       '## 22. Three Levels of Visual Fidelity\n'
                       '\n'
                       'The source compares three system designs.\n'
                       '\n'
                       'A **text-only baseline** ignores images, so it fails when the answer '
                       'exists only in a chart.\n'
                       '\n'
                       'A **summary-enhanced system** retrieves image descriptions and can often '
                       'answer qualitative questions about trends.\n'
                       '\n'
                       'A **raw-image generation system** can inspect the actual chart and may '
                       'recover fine-grained values that were absent from the summary.\n'
                       '\n'
                       'This comparison is important because it demonstrates that multimodal RAG '
                       'is not binary. You can incrementally add fidelity according to product '
                       'requirements and cost budgets.\n'
                       '\n'
                       '## 23. Shared Text–Image Embedding Spaces\n'
                       '\n'
                       'Instead of translating every image into text, a multimodal embedding model '
                       'can map images and text into a shared vector space.\n'
                       '\n'
                       'The model uses separate encoders for each modality but trains them so '
                       'semantically corresponding pairs become close in the common space. A text '
                       'query such as “red sports car” can therefore retrieve an image even if the '
                       'image contains no caption with those words.\n'
                       '\n'
                       'This is cross-modal retrieval: query and candidate do not need to share '
                       'the same input modality as long as their embeddings inhabit the same '
                       'semantic geometry.\n'
                       '\n'
                       '{{exercise:M01.L08.EX09}}\n'
                       '\n'
                       '[[IMAGE_NEEDED: Shared text-image embedding space | Text encoder and image '
                       'encoder mapping matched concepts into nearby vectors | Notice that '
                       'different modalities become directly comparable]]\n'
                       '\n'
                       '## 24. Contrastive Learning Intuition\n'
                       '\n'
                       'Shared embedding models are often trained using contrastive objectives.\n'
                       '\n'
                       'Given matching image–text pairs, training pulls the matched vectors closer '
                       'while pushing mismatched pairs farther apart. The result is not a symbolic '
                       'description of every detail in an image; it is a representation optimized '
                       'for matching semantically related items.\n'
                       '\n'
                       'That distinction explains both the strength and weakness of these models. '
                       'They are excellent for finding conceptually related visuals, but a single '
                       'embedding vector may not preserve every tiny number on a chart.\n'
                       '\n'
                       '## 25. SigLIP Retrieval: What the Example Demonstrates\n'
                       '\n'
                       'The chapter uses SigLIP to encode images and a text query into a shared '
                       'space. Both feature vectors are normalized, then compared using a dot '
                       'product.\n'
                       '\n'
                       'For unit-normalized vectors:\n'
                       '\n'
                       '**dot product = cosine similarity**\n'
                       '\n'
                       'A simplified retrieval pattern is:\n'
                       '\n'
                       '```python\n'
                       'image_vecs = normalize(model.encode_images(images))\n'
                       'query_vec = normalize(model.encode_text(query))\n'
                       'scores = query_vec @ image_vecs.T\n'
                       'top_ids = scores.topk(k).indices\n'
                       '```\n'
                       '\n'
                       'The example is deliberately small and uses exact comparison. A production '
                       'collection would store the image embeddings in a vector database and use '
                       'an ANN index.\n'
                       '\n'
                       '## 26. Where Shared Embeddings Shine\n'
                       '\n'
                       'Shared embeddings are particularly effective for visual search across '
                       'photos, slides, product catalogs, and other visually descriptive '
                       'collections.\n'
                       '\n'
                       'They can match concepts, styles, and aesthetics even when the user query '
                       'and image share no exact keywords. This makes them useful for queries such '
                       'as “modern living room with natural light” or “round cheese pizza.”\n'
                       '\n'
                       'They also reduce ingestion dependence on expensive VLM captioning for '
                       'every image because the image encoder directly creates the searchable '
                       'representation.\n'
                       '\n'
                       '## 27. Where Shared Embeddings Struggle\n'
                       '\n'
                       'A visual embedding optimized for semantic matching is not necessarily a '
                       'precise representation of all visual facts.\n'
                       '\n'
                       'Information-dense charts, schematics, forms, and diagrams may contain '
                       'exact numbers or fine relationships that are not preserved in a single '
                       'vector. The model may know “this is a sales chart” without encoding the '
                       'exact Q3 revenue.\n'
                       '\n'
                       'Shared visual embeddings also complicate standard hybrid search because '
                       'images have no lexical tokens for BM25, and conventional text '
                       'cross-encoders cannot rerank image–text pairs directly.\n'
                       '\n'
                       'For fine-grained reasoning, summary-based retrieval or raw-image '
                       'inspection may still be preferable.\n'
                       '\n'
                       '{{exercise:M01.L08.EX10}}\n'
                       '\n'
                       '## 28. Hybrid Multimodal Architectures\n'
                       '\n'
                       'Production systems often combine strategies instead of choosing one '
                       'exclusively.\n'
                       '\n'
                       'An image can have:\n'
                       '\n'
                       '- a raw object in object storage,\n'
                       '- a detailed VLM-generated caption,\n'
                       '- a multimodal embedding,\n'
                       '- OCR text,\n'
                       '- document/page metadata.\n'
                       '\n'
                       'Different retrieval channels can search different representations, and a '
                       'fusion stage can combine candidates. This increases engineering '
                       'complexity, but it provides better coverage across exact text, semantic '
                       'concepts, and visual similarity.\n'
                       '\n'
                       'The same principle applies to tables and video: maintain multiple '
                       'representations when each serves a distinct retrieval or reasoning '
                       'purpose.\n'
                       '\n'
                       '## 29. Audio and Video as RAG Knowledge Sources\n'
                       '\n'
                       'Audio and video contain two kinds of information: *what was said* and '
                       '*what was shown or how it was said*.\n'
                       '\n'
                       'The simplest production path is to convert speech to text, but good '
                       'multimedia RAG retains speaker identity and timestamps so retrieved facts '
                       'can be attributed and linked back to the original media.\n'
                       '\n'
                       'For video, transcription alone is insufficient when meaning depends on '
                       'visual actions. A technician saying “press this” has little semantic value '
                       'unless the system also captures which control was pressed.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Multimedia RAG timeline | Audio waveform/video track -> '
                       'ASR + diarization + timestamps + frame/segment extraction -> indexed '
                       'evidence | Notice provenance is preserved through timecodes]]\n'
                       '\n'
                       '## 30. High-Fidelity ASR as the Baseline\n'
                       '\n'
                       'Automatic speech recognition turns audio into text and allows the rest of '
                       'the RAG stack to reuse familiar text retrieval machinery.\n'
                       '\n'
                       'A production transcript should preserve at least:\n'
                       '\n'
                       '- the spoken text,\n'
                       '- speaker identity when possible,\n'
                       '- start and end timestamps,\n'
                       '- confidence or quality metadata when available.\n'
                       '\n'
                       'These fields support speaker-aware filtering, source verification, deep '
                       'links into the media player, and later redaction workflows.\n'
                       '\n'
                       '## 31. Why Speaker Diarization Matters\n'
                       '\n'
                       'Speaker diarization answers *who spoke when*.\n'
                       '\n'
                       'A flat transcript can turn a dialogue into an ambiguous block of text. In '
                       'business calls, the identity of the speaker may determine the importance '
                       'or authority of a statement. A commitment from a customer is different '
                       'from a suggestion by an agent.\n'
                       '\n'
                       'Diarization metadata makes retrieved evidence more useful because the '
                       'system can return not only the words but also the speaker and location in '
                       'the recording.\n'
                       '\n'
                       '{{exercise:M01.L08.EX11}}\n'
                       '\n'
                       '## 32. Chunking Transcripts Without Losing Dialogue Structure\n'
                       '\n'
                       'Transcript chunking should preserve conversational coherence.\n'
                       '\n'
                       'A practical strategy is to accumulate several utterances until a target '
                       'size is reached, while keeping sentence boundaries intact. Each chunk '
                       'carries the earliest timestamp, latest timestamp, and set of speakers '
                       'represented inside it.\n'
                       '\n'
                       'Unlike prose chunking, the metadata is not optional decoration. It is part '
                       'of the evidence model because users may want to ask “What did the customer '
                       'say?” rather than merely “What was said?”\n'
                       '\n'
                       '## 33. ASR Pipeline Example: Lessons from Deepgram\n'
                       '\n'
                       'The chapter uses a speech-to-text service with diarization enabled, then '
                       'groups returned utterances into retrieval chunks.\n'
                       '\n'
                       'A simplified version is:\n'
                       '\n'
                       '```python\n'
                       'chunks = []\n'
                       'buffer = []\n'
                       '\n'
                       'for utterance in transcript.utterances:\n'
                       '    buffer.append({\n'
                       '        "speaker": utterance.speaker,\n'
                       '        "text": utterance.text,\n'
                       '        "start": utterance.start,\n'
                       '        "end": utterance.end,\n'
                       '    })\n'
                       '\n'
                       '    if token_estimate(buffer) >= TARGET_SIZE:\n'
                       '        chunks.append(build_chunk(buffer))\n'
                       '        buffer = []\n'
                       '```\n'
                       '\n'
                       'The architectural lesson is service-independent: convert media into '
                       'semantically coherent text plus provenance metadata, then index that '
                       'representation.\n'
                       '\n'
                       '## 34. Designing Jump-to-Source Multimedia UX\n'
                       '\n'
                       'Timestamps enable a powerful trust feature: the answer can link directly '
                       'to the relevant moment in the original recording or video.\n'
                       '\n'
                       'This is the multimedia equivalent of page-number citations in document '
                       'RAG. It reduces verification cost for users because they do not need to '
                       'search through a one-hour recording manually.\n'
                       '\n'
                       'A good retrieval result therefore stores provenance granular enough for '
                       'the frontend to construct a deep link, not merely a filename.\n'
                       '\n'
                       '## 35. The Red-Button Problem\n'
                       '\n'
                       'Consider a training video in which a technician says, “Now do this,” while '
                       'pressing a red emergency-stop control.\n'
                       '\n'
                       'The transcript captures the words but not the referent of “this.” If a '
                       'user later asks how to stop the machine, text-only retrieval may fail '
                       'completely.\n'
                       '\n'
                       'This example illustrates **silent semantics**: information communicated '
                       'visually rather than verbally. Video RAG needs some representation of '
                       'frames or temporal segments so visual actions become searchable evidence.\n'
                       '\n'
                       '{{exercise:M01.L08.EX12}}\n'
                       '\n'
                       '[[IMAGE_NEEDED: The red-button problem | Video frame showing technician '
                       "pressing a red emergency stop while transcript says 'do this' | Notice why "
                       'transcript-only retrieval loses the referent]]\n'
                       '\n'
                       '## 36. Fixed-Interval Frame Extraction\n'
                       '\n'
                       'The simplest visual-video strategy samples frames at a regular interval, '
                       'such as one frame per second.\n'
                       '\n'
                       'Each frame can be captioned with a VLM or embedded with a visual encoder. '
                       'The resulting timeline gives high temporal granularity and can identify '
                       'objects or scenes precisely.\n'
                       '\n'
                       'The disadvantage is cost and redundancy. Long videos generate many nearly '
                       'identical frames, consuming storage, embedding compute, and potentially '
                       'captioning API calls.\n'
                       '\n'
                       '## 37. Temporal Segment Extraction\n'
                       '\n'
                       'Some questions concern actions that unfold over time rather than static '
                       'objects.\n'
                       '\n'
                       'Instead of analyzing isolated frames, a system can cut video into '
                       'overlapping segments and send each segment to a temporal-aware '
                       'vision-language model. The generated description can capture sequences and '
                       'causality, such as one action occurring before another.\n'
                       '\n'
                       'This is more computationally expensive but better for procedures, '
                       'behavior, and motion-dependent meaning.\n'
                       '\n'
                       '## 38. Keyframe Extraction\n'
                       '\n'
                       'Keyframe extraction reduces cost by processing only moments where the '
                       'scene changes meaningfully.\n'
                       '\n'
                       'A scene-detection step identifies visually significant transitions. Only '
                       'those frames are captioned or embedded, and the resulting description can '
                       'be merged with nearby transcript text.\n'
                       '\n'
                       'Keyframes are often a strong compromise between the dense coverage of '
                       'fixed sampling and the high expense of segment-level video understanding.\n'
                       '\n'
                       '## 39. Choosing a Video Extraction Strategy\n'
                       '\n'
                       'There is no universally correct video representation.\n'
                       '\n'
                       'Choose **fixed frames** when object-level visual recall and precise '
                       'timestamps matter.\n'
                       '\n'
                       'Choose **temporal segments** when actions and sequences matter.\n'
                       '\n'
                       'Choose **keyframes** when cost is important and scene changes capture most '
                       'useful information.\n'
                       '\n'
                       'A mature system can combine them—for example, inexpensive frames for broad '
                       'retrieval and expensive segment analysis only for high-value or ambiguous '
                       'content.\n'
                       '\n'
                       '{{exercise:M01.L08.EX13}}\n'
                       '\n'
                       '## 40. Computational Economics and Latency\n'
                       '\n'
                       'Multimodal pipelines can be far more expensive than text pipelines.\n'
                       '\n'
                       'At ingestion time, OCR, image captioning, multimodal embeddings, ASR, and '
                       'video frame processing increase compute and API usage. At query time, '
                       'loading images or video into a multimodal generator increases '
                       'token-equivalent processing and latency.\n'
                       '\n'
                       'This makes caching, routing, batching, and precomputation especially '
                       'important. The conversion approach is often attractive because it shifts '
                       'expensive interpretation to ingestion and allows many queries to reuse the '
                       'resulting representations.\n'
                       '\n'
                       '{{exercise:M01.L08.EX14}}\n'
                       '\n'
                       '## 41. Modality Alignment\n'
                       '\n'
                       'Different representations of the same source must remain aligned.\n'
                       '\n'
                       'A table summary must point to the correct table. An image caption must '
                       'point to the correct page and image. A transcript chunk must point to the '
                       'correct timestamp. A video caption must correspond to the correct '
                       'segment.\n'
                       '\n'
                       'Alignment bugs can be worse than retrieval misses because they create '
                       'plausible but incorrect evidence chains. Production systems need stable '
                       'IDs, provenance metadata, and validation checks across every conversion stage.\n\n{{image:modality-alignment}}'
                       '\n'
                       '\n'
                       '## 42. The Interface Layer: Visual Citations\n'
                       '\n'
                       'Multimodal RAG should make evidence inspectable.\n'
                       '\n'
                       'For tables, a citation can open the source page and highlight the relevant '
                       'table. For images, the UI can show a thumbnail or full-resolution visual '
                       'next to the answer. For audio and video, a citation can jump to the exact '
                       'timestamp.\n'
                       '\n'
                       'This is not merely a frontend convenience. Strong source navigation '
                       'improves trust, debugging, user feedback, and evaluation because humans '
                       'can verify what the model used.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Multimodal citation UI | Answer with links to table '
                       'cell/page, image thumbnail, and audio/video timestamp | Notice how every '
                       'claim can be inspected at its original source]]\n'
                       '\n'
                       '## 43. Security, Privacy, and Governance\n'
                       '\n'
                       'Every new modality expands the attack and privacy surface.\n'
                       '\n'
                       'Images may contain faces, IDs, or confidential screenshots. Audio may '
                       'contain names, account numbers, or health information. Video may capture '
                       'people who did not expect automated indexing.\n'
                       '\n'
                       'The same governance principles from text RAG still apply—access control, '
                       'encryption, retention, redaction, auditability—but extraction makes them '
                       'harder because sensitive information may exist in pixels or speech rather '
                       'than explicit text fields.\n'
                       '\n'
                       '## 44. Visual Prompt Injection\n'
                       '\n'
                       'Images can contain text that attempts to influence a vision-language '
                       'model—for example, hidden or small instructions telling the model to '
                       'ignore the user’s task.\n'
                       '\n'
                       'That is the visual counterpart of indirect prompt injection in document '
                       'RAG.\n'
                       '\n'
                       'Defenses should treat extracted visual text and captions as untrusted '
                       'data, maintain strong instruction boundaries, limit tool privileges, and '
                       'validate high-risk actions independently of content retrieved from '
                       'documents or images.\n'
                       '\n'
                       '{{exercise:M01.L08.EX15}}\n'
                       '\n'
                       '## 45. Unstructured PII Leakage\n'
                       '\n'
                       'Multimodal data can expose sensitive information that ordinary '
                       'text-redaction pipelines never see.\n'
                       '\n'
                       'A screenshot may contain an email address, an ID card, or account data. A '
                       'recording may reveal names or health details. OCR and ASR can make these '
                       'values machine-readable only *after* ingestion has already processed the '
                       'raw media.\n'
                       '\n'
                       'Therefore, privacy controls may need to operate both before storage of raw '
                       'media and after extraction of text. Retention policies should account for '
                       'the original binary object as well as every derived representation.\n'
                       '\n'
                       '## 46. Deep Observability for Multimodal Pipelines\n'
                       '\n'
                       'A multimodal ingestion trace should expose each transformation, not only '
                       'the final vector-store insertion.\n'
                       '\n'
                       'For an image, record extraction success, caption model, caption text, '
                       'embedding model, object-store ID, page provenance, and validation status.\n'
                       '\n'
                       'For audio, record ASR model, diarization result, timestamps, confidence, '
                       'chunk IDs, and any redaction.\n'
                       '\n'
                       'Without this visibility, a wrong answer becomes nearly impossible to '
                       'diagnose because the error may originate in parsing, captioning, '
                       'representation, retrieval, or generation.\n'
                       '\n'
                       '## 47. How Multimodal Hallucinations Arise\n'
                       '\n'
                       'Multimodal RAG adds new failure modes on top of ordinary RAG.\n'
                       '\n'
                       'A VLM may invent a value that is not visible in a chart. OCR may misread a '
                       'label. An image summary may omit a key detail. A transcript may assign '
                       'speech to the wrong speaker. A video caption may describe an action that '
                       'did not occur.\n'
                       '\n'
                       'The final answer may then be perfectly faithful to a *bad derived '
                       'representation*. This is why evaluation must separate source extraction '
                       'quality from retrieval quality and generation quality.\n'
                       '\n'
                       '{{exercise:M01.L08.EX16}}\n'
                       '\n'
                       '## 48. Detecting Multimodal Hallucinations\n'
                       '\n'
                       'Hallucination checks should compare the generated claim to the underlying '
                       'modality whenever possible, not only to the converted text.\n'
                       '\n'
                       'For example, an answer derived from a chart summary may appear faithful to '
                       'the summary even if the summary itself was wrong. A stronger evaluator can '
                       'inspect the original chart and determine whether the answer is visually '
                       'supported.\n'
                       '\n'
                       'This is more expensive, but it provides a more truthful measure of '
                       'end-to-end faithfulness.\n'
                       '\n'
                       '## 49. Evaluating Multimodal Retrieval\n'
                       '\n'
                       'Retrieval evaluation still asks whether the system surfaced the evidence '
                       'required to answer the query.\n'
                       '\n'
                       'Metrics such as recall@k remain useful, but the relevance labels may now '
                       'refer to tables, images, audio segments, or video segments rather than '
                       'text chunks.\n'
                       '\n'
                       'A multimodal benchmark should include queries whose answers genuinely '
                       'depend on non-text evidence. Otherwise, a system could score well while '
                       'silently failing on the very modalities it claims to support.\n'
                       '\n'
                       '{{exercise:M01.L08.EX17}}\n'
                       '\n'
                       '## 50. Evaluating Generation with a VLM-as-a-Judge\n'
                       '\n'
                       'For responses grounded in images or video, a text-only judge may be unable '
                       'to determine whether the answer is faithful.\n'
                       '\n'
                       'A vision-language judge can receive the original visual evidence, the user '
                       'query, and the generated answer, then assess factual consistency and '
                       'relevance.\n'
                       '\n'
                       'As with LLM-as-a-judge, the evaluator itself can be biased or unstable. '
                       'Use clear rubrics, representative test sets, repeated measurements where '
                       'needed, and human calibration for important domains.\n'
                       '\n'
                       '## 51. Build Evaluation at Every Representation Boundary\n'
                       '\n'
                       'A robust multimodal evaluation suite should test more than the final '
                       'answer.\n'
                       '\n'
                       'For tables: validate extracted shapes, headers, cell values, stitching, '
                       'retrieval, and answer fidelity.\n'
                       '\n'
                       'For images: validate extraction, caption quality, cross-modal retrieval, '
                       'and visual grounding.\n'
                       '\n'
                       'For audio/video: validate transcription, speaker attribution, timestamps, '
                       'visual extraction, retrieval, and final answer quality.\n'
                       '\n'
                       'This layered evaluation makes root-cause analysis possible. Without it, a '
                       'single end-to-end score tells you that the system failed but not *where*.\n'
                       '\n'
                       '## 52. Decision Guide for Table Architectures\n'
                       '\n'
                       'Use row-level representations when questions usually target individual '
                       'records and row context is sufficient.\n'
                       '\n'
                       'Use the summary-pointer pattern when users ask broad questions that '
                       'require table-wide understanding or when tables are large.\n'
                       '\n'
                       'Use full structured tables at generation time when precise cross-column '
                       'reasoning is required.\n'
                       '\n'
                       'Use conditional parsers and validation when document layouts vary '
                       'significantly.\n'
                       '\n'
                       'The best architecture is determined by the query workload, not by a '
                       'generic table-processing rule.\n'
                       '\n'
                       '## 53. Decision Guide for Image Architectures\n'
                       '\n'
                       'Use image summaries when query-time speed and compatibility with text '
                       'infrastructure matter most.\n'
                       '\n'
                       'Use shared multimodal embeddings when users search primarily by visual '
                       'concepts or style.\n'
                       '\n'
                       'Use summary retrieval plus raw-image generation when you need both '
                       'efficient search and fine-grained visual reasoning.\n'
                       '\n'
                       'For information-dense charts or diagrams, prefer approaches that let the '
                       'generator inspect the original visual evidence instead of relying on a '
                       'single compressed vector.\n'
                       '\n'
                       '## 54. Decision Guide for Audio and Video Architectures\n'
                       '\n'
                       'For audio-focused collections, start with high-quality ASR, diarization, '
                       'timestamps, and transcript chunking.\n'
                       '\n'
                       'For videos where visuals are secondary, combine transcripts with keyframe '
                       'captions.\n'
                       '\n'
                       'For procedural or motion-heavy video, use temporal segment understanding '
                       'for the portions where sequence matters.\n'
                       '\n'
                       'Always preserve source timecodes so answers can link back to the media and '
                       'be independently verified.\n'
                       '\n'
                       '## 55. A Production Multimodal RAG Blueprint\n'
                       '\n'
                       'A practical production design can separate responsibilities into '
                       'specialized services:\n'
                       '\n'
                       '1. **Ingestion router** identifies modality and document type.\n'
                       '2. **Text/parser service** extracts ordinary text.\n'
                       '3. **Table service** detects, normalizes, validates, and stores structured '
                       'tables.\n'
                       '4. **Vision service** extracts images and produces captions or '
                       'embeddings.\n'
                       '5. **ASR/video service** produces timestamped transcript and visual '
                       'representations.\n'
                       '6. **Representation store** holds raw objects, structured data, and '
                       'metadata.\n'
                       '7. **Search layer** indexes text and multimodal vectors.\n'
                       '8. **Retriever/reranker** produces evidence candidates.\n'
                       '9. **Generator** consumes text, structured data, and raw visuals when '
                       'needed.\n'
                       '10. **Citation layer** maps claims back to pages, objects, and '
                       'timestamps.\n'
                       '11. **Evaluation/observability** monitors quality at every '
                       'transformation.\n'
                       '\n'
                       'The blueprint is intentionally modular because each modality has different '
                       'failure modes and scaling characteristics.\n'
                       '\n'
                       '{{exercise:M01.L08.EX18}}\n'
                       '\n'
                       '[[IMAGE_NEEDED: Production multimodal RAG architecture | Modality router '
                       'feeding text, table, image, ASR/video processors into stores, retrieval, '
                       'generator, citations, evaluation | Notice separate modality processing but '
                       'shared query orchestration]]\n'
                       '\n'
                       '## 56. Common Multimodal RAG Mistakes\n'
                       '\n'
                       'Several mistakes recur across multimodal projects.\n'
                       '\n'
                       '**Mistake 1: treating OCR text as equivalent to the original object.** OCR '
                       'may lose structure.\n'
                       '\n'
                       '**Mistake 2: chunking tables like prose.** This separates values from '
                       'headers.\n'
                       '\n'
                       '**Mistake 3: trusting parser output without validation.** Empty or '
                       'malformed tables are normal failure cases.\n'
                       '\n'
                       '**Mistake 4: embedding only image captions and discarding originals.** '
                       'This makes lost details unrecoverable.\n'
                       '\n'
                       '**Mistake 5: transcribing video and ignoring visuals.** Silent semantics '
                       'disappear.\n'
                       '\n'
                       '**Mistake 6: storing media without precise provenance.** Users cannot '
                       'verify answers.\n'
                       '\n'
                       '**Mistake 7: evaluating only final answers.** Representation failures '
                       'remain invisible.\n'
                       '\n'
                       'A useful rule is: every conversion step is a possible information-loss '
                       'boundary, so every boundary deserves validation.\n'
                       '\n'
                       '## 57. Terminology You Should Retain\n'
                       '\n'
                       '| Term | Meaning in this lesson |\n'
                       '|---|---|\n'
                       '| Multimodal RAG | RAG that grounds answers in more than plain text |\n'
                       '| Conversion approach | Transform non-text data into text/structured '
                       'representations |\n'
                       '| Native multimodal approach | Represent and reason over multiple '
                       'modalities directly |\n'
                       '| VLM | Vision–language model |\n'
                       '| OCR | Optical character recognition |\n'
                       '| ASR | Automatic speech recognition |\n'
                       '| Diarization | Identifying who spoke when |\n'
                       '| Shared embedding space | Vector space where different modalities are '
                       'directly comparable |\n'
                       '| Contrastive learning | Training matched representations to be close and '
                       'mismatched ones to be distant |\n'
                       '| Keyframe | Representative frame chosen around a meaningful visual change '
                       '|\n'
                       '| Temporal segment | Video interval analyzed as a sequence rather than '
                       'isolated frames |\n'
                       '| Summary-pointer pattern | Retrieve a compact summary that points to a '
                       'richer source object |\n'
                       '| Visual citation | Citation that links to a table, image, frame, or media '
                       'timestamp |\n'
                       '\n'
                       '## 58. Retain This Mental Model\n'
                       '\n'
                       'Multimodal RAG is fundamentally about **preserving evidence across '
                       'representation changes**.\n'
                       '\n'
                       'A table is not a bag of numbers. An image is not merely OCR text. A '
                       'recording is not merely a transcript. A video is not merely a sequence of '
                       'frames.\n'
                       '\n'
                       'Every modality contains relationships that can disappear during '
                       'conversion. The system designer’s job is to preserve enough of those '
                       'relationships to make retrieval useful, keep the original evidence '
                       'available when higher fidelity is needed, and expose provenance so users '
                       'can verify the answer.\n'
                       '\n'
                       'If you remember only one architecture pattern, remember this:\n'
                       '\n'
                       '**retrieve with the cheapest representation that preserves recall; reason '
                       'with the richest representation needed for fidelity; cite the original '
                       'evidence.**\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Comprehensive self-check\n'
                       '\n'
                       'Use the questions below without looking back at the lesson. If you cannot '
                       'answer one precisely, revisit the relevant section before moving on.\n'
                       '\n'
                       '1. What problem does **Why Multimodal RAG Matters** solve in a multimodal '
                       'RAG system?\n'
                       '2. What information could be lost if **Why Multimodal RAG Matters** is '
                       'implemented poorly?\n'
                       '3. What production trade-off or validation check is most important for '
                       '**Why Multimodal RAG Matters**?\n'
                       '4. What problem does **Conversion Versus Native Multimodal RAG** solve in '
                       'a multimodal RAG system?\n'
                       '5. What information could be lost if **Conversion Versus Native Multimodal '
                       'RAG** is implemented poorly?\n'
                       '6. What production trade-off or validation check is most important for '
                       '**Conversion Versus Native Multimodal RAG**?\n'
                       '7. What problem does **Design Principle: Preserve Semantics, Not Just '
                       'Bytes** solve in a multimodal RAG system?\n'
                       '8. What information could be lost if **Design Principle: Preserve '
                       'Semantics, Not Just Bytes** is implemented poorly?\n'
                       '9. What production trade-off or validation check is most important for '
                       '**Design Principle: Preserve Semantics, Not Just Bytes**?\n'
                       '10. What problem does **Tables as Semantic Micro-Documents** solve in a '
                       'multimodal RAG system?\n'
                       '11. What information could be lost if **Tables as Semantic '
                       'Micro-Documents** is implemented poorly?\n'
                       '12. What production trade-off or validation check is most important for '
                       '**Tables as Semantic Micro-Documents**?\n'
                       '13. What problem does **The Three Stages of Table Extraction** solve in a '
                       'multimodal RAG system?\n'
                       '14. What information could be lost if **The Three Stages of Table '
                       'Extraction** is implemented poorly?\n'
                       '15. What production trade-off or validation check is most important for '
                       '**The Three Stages of Table Extraction**?\n'
                       '16. What problem does **Choosing Table Extraction Tools** solve in a '
                       'multimodal RAG system?\n'
                       '17. What information could be lost if **Choosing Table Extraction Tools** '
                       'is implemented poorly?\n'
                       '18. What production trade-off or validation check is most important for '
                       '**Choosing Table Extraction Tools**?\n'
                       '19. What problem does **Table Extraction with Docling: What the Example '
                       'Teaches** solve in a multimodal RAG system?\n'
                       '20. What information could be lost if **Table Extraction with Docling: '
                       'What the Example Teaches** is implemented poorly?\n'
                       '21. What production trade-off or validation check is most important for '
                       '**Table Extraction with Docling: What the Example Teaches**?\n'
                       '22. What problem does **Parser Failure Is Normal—Design for It** solve in '
                       'a multimodal RAG system?\n'
                       '23. What information could be lost if **Parser Failure Is Normal—Design '
                       'for It** is implemented poorly?\n'
                       '24. What production trade-off or validation check is most important for '
                       '**Parser Failure Is Normal—Design for It**?\n'
                       '25. What problem does **Conditional Parsing Pipelines** solve in a '
                       'multimodal RAG system?\n'
                       '26. What information could be lost if **Conditional Parsing Pipelines** is '
                       'implemented poorly?\n'
                       '27. What production trade-off or validation check is most important for '
                       '**Conditional Parsing Pipelines**?\n'
                       '28. What problem does **Why Naive Chunking Breaks Tables** solve in a '
                       'multimodal RAG system?\n'
                       '29. What information could be lost if **Why Naive Chunking Breaks Tables** '
                       'is implemented poorly?\n'
                       '30. What production trade-off or validation check is most important for '
                       '**Why Naive Chunking Breaks Tables**?\n'
                       '31. What problem does **Represent Tables as Structured Context** solve in '
                       'a multimodal RAG system?\n'
                       '32. What information could be lost if **Represent Tables as Structured '
                       'Context** is implemented poorly?\n'
                       '33. What production trade-off or validation check is most important for '
                       '**Represent Tables as Structured Context**?\n'
                       '34. What problem does **The Summary-Pointer Pattern for Tables** solve in '
                       'a multimodal RAG system?\n'
                       '35. What information could be lost if **The Summary-Pointer Pattern for '
                       'Tables** is implemented poorly?\n'
                       '36. What production trade-off or validation check is most important for '
                       '**The Summary-Pointer Pattern for Tables**?\n'
                       '37. What problem does **Prompting with Mixed Text and Structured Data** '
                       'solve in a multimodal RAG system?\n'
                       '38. What information could be lost if **Prompting with Mixed Text and '
                       'Structured Data** is implemented poorly?\n'
                       '39. What production trade-off or validation check is most important for '
                       '**Prompting with Mixed Text and Structured Data**?\n'
                       '40. What problem does **Why Multi-Page Tables Are a Special Case** solve '
                       'in a multimodal RAG system?\n'
                       '41. What information could be lost if **Why Multi-Page Tables Are a '
                       'Special Case** is implemented poorly?\n'
                       '42. What production trade-off or validation check is most important for '
                       '**Why Multi-Page Tables Are a Special Case**?\n'
                       '43. What problem does **A Practical Table-Stitching Heuristic** solve in a '
                       'multimodal RAG system?\n'
                       '44. What information could be lost if **A Practical Table-Stitching '
                       'Heuristic** is implemented poorly?\n'
                       '45. What production trade-off or validation check is most important for '
                       '**A Practical Table-Stitching Heuristic**?\n'
                       '46. What problem does **End-to-End Table RAG Flow** solve in a multimodal '
                       'RAG system?\n'
                       '47. What information could be lost if **End-to-End Table RAG Flow** is '
                       'implemented poorly?\n'
                       '48. What production trade-off or validation check is most important for '
                       '**End-to-End Table RAG Flow**?\n'
                       '49. What problem does **Why Images Need More Than OCR** solve in a '
                       'multimodal RAG system?\n'
                       '50. What information could be lost if **Why Images Need More Than OCR** is '
                       'implemented poorly?\n'
                       '51. What production trade-off or validation check is most important for '
                       '**Why Images Need More Than OCR**?\n'
                       '52. What problem does **Two Main Image Strategies** solve in a multimodal '
                       'RAG system?\n'
                       '53. What information could be lost if **Two Main Image Strategies** is '
                       'implemented poorly?\n'
                       '54. What production trade-off or validation check is most important for '
                       '**Two Main Image Strategies**?\n'
                       '55. What problem does **Image Summarization During Ingestion** solve in a '
                       'multimodal RAG system?\n'
                       '56. What information could be lost if **Image Summarization During '
                       'Ingestion** is implemented poorly?\n'
                       '57. What production trade-off or validation check is most important for '
                       '**Image Summarization During Ingestion**?\n'
                       '58. What problem does **The Information Bottleneck of Image Summaries** '
                       'solve in a multimodal RAG system?\n'
                       '59. What information could be lost if **The Information Bottleneck of '
                       'Image Summaries** is implemented poorly?\n'
                       '60. What production trade-off or validation check is most important for '
                       '**The Information Bottleneck of Image Summaries**?\n'
                       '61. What problem does **Retrieve by Summary, Reason over the Original '
                       'Image** solve in a multimodal RAG system?\n'
                       '62. What information could be lost if **Retrieve by Summary, Reason over '
                       'the Original Image** is implemented poorly?\n'
                       '63. What production trade-off or validation check is most important for '
                       '**Retrieve by Summary, Reason over the Original Image**?\n'
                       '64. What problem does **Three Levels of Visual Fidelity** solve in a '
                       'multimodal RAG system?\n'
                       '65. What information could be lost if **Three Levels of Visual Fidelity** '
                       'is implemented poorly?\n'
                       '66. What production trade-off or validation check is most important for '
                       '**Three Levels of Visual Fidelity**?\n'
                       '67. What problem does **Shared Text–Image Embedding Spaces** solve in a '
                       'multimodal RAG system?\n'
                       '68. What information could be lost if **Shared Text–Image Embedding '
                       'Spaces** is implemented poorly?\n'
                       '69. What production trade-off or validation check is most important for '
                       '**Shared Text–Image Embedding Spaces**?\n'
                       '70. What problem does **Contrastive Learning Intuition** solve in a '
                       'multimodal RAG system?\n'
                       '71. What information could be lost if **Contrastive Learning Intuition** '
                       'is implemented poorly?\n'
                       '72. What production trade-off or validation check is most important for '
                       '**Contrastive Learning Intuition**?\n'
                       '73. What problem does **SigLIP Retrieval: What the Example Demonstrates** '
                       'solve in a multimodal RAG system?\n'
                       '74. What information could be lost if **SigLIP Retrieval: What the Example '
                       'Demonstrates** is implemented poorly?\n'
                       '75. What production trade-off or validation check is most important for '
                       '**SigLIP Retrieval: What the Example Demonstrates**?\n'
                       '76. What problem does **Where Shared Embeddings Shine** solve in a '
                       'multimodal RAG system?\n'
                       '77. What information could be lost if **Where Shared Embeddings Shine** is '
                       'implemented poorly?\n'
                       '78. What production trade-off or validation check is most important for '
                       '**Where Shared Embeddings Shine**?\n'
                       '79. What problem does **Where Shared Embeddings Struggle** solve in a '
                       'multimodal RAG system?\n'
                       '80. What information could be lost if **Where Shared Embeddings Struggle** '
                       'is implemented poorly?\n'
                       '81. What production trade-off or validation check is most important for '
                       '**Where Shared Embeddings Struggle**?\n'
                       '82. What problem does **Hybrid Multimodal Architectures** solve in a '
                       'multimodal RAG system?\n'
                       '83. What information could be lost if **Hybrid Multimodal Architectures** '
                       'is implemented poorly?\n'
                       '84. What production trade-off or validation check is most important for '
                       '**Hybrid Multimodal Architectures**?\n'
                       '85. What problem does **Audio and Video as RAG Knowledge Sources** solve '
                       'in a multimodal RAG system?\n'
                       '86. What information could be lost if **Audio and Video as RAG Knowledge '
                       'Sources** is implemented poorly?\n'
                       '87. What production trade-off or validation check is most important for '
                       '**Audio and Video as RAG Knowledge Sources**?\n'
                       '88. What problem does **High-Fidelity ASR as the Baseline** solve in a '
                       'multimodal RAG system?\n'
                       '89. What information could be lost if **High-Fidelity ASR as the '
                       'Baseline** is implemented poorly?\n'
                       '90. What production trade-off or validation check is most important for '
                       '**High-Fidelity ASR as the Baseline**?\n'
                       '91. What problem does **Why Speaker Diarization Matters** solve in a '
                       'multimodal RAG system?\n'
                       '92. What information could be lost if **Why Speaker Diarization Matters** '
                       'is implemented poorly?\n'
                       '93. What production trade-off or validation check is most important for '
                       '**Why Speaker Diarization Matters**?\n'
                       '94. What problem does **Chunking Transcripts Without Losing Dialogue '
                       'Structure** solve in a multimodal RAG system?\n'
                       '95. What information could be lost if **Chunking Transcripts Without '
                       'Losing Dialogue Structure** is implemented poorly?\n'
                       '96. What production trade-off or validation check is most important for '
                       '**Chunking Transcripts Without Losing Dialogue Structure**?\n'
                       '97. What problem does **ASR Pipeline Example: Lessons from Deepgram** '
                       'solve in a multimodal RAG system?\n'
                       '98. What information could be lost if **ASR Pipeline Example: Lessons from '
                       'Deepgram** is implemented poorly?\n'
                       '99. What production trade-off or validation check is most important for '
                       '**ASR Pipeline Example: Lessons from Deepgram**?\n'
                       '100. What problem does **Designing Jump-to-Source Multimedia UX** solve in '
                       'a multimodal RAG system?\n'
                       '101. What information could be lost if **Designing Jump-to-Source '
                       'Multimedia UX** is implemented poorly?\n'
                       '102. What production trade-off or validation check is most important for '
                       '**Designing Jump-to-Source Multimedia UX**?\n'
                       '103. What problem does **The Red-Button Problem** solve in a multimodal '
                       'RAG system?\n'
                       '104. What information could be lost if **The Red-Button Problem** is '
                       'implemented poorly?\n'
                       '105. What production trade-off or validation check is most important for '
                       '**The Red-Button Problem**?\n'
                       '106. What problem does **Fixed-Interval Frame Extraction** solve in a '
                       'multimodal RAG system?\n'
                       '107. What information could be lost if **Fixed-Interval Frame Extraction** '
                       'is implemented poorly?\n'
                       '108. What production trade-off or validation check is most important for '
                       '**Fixed-Interval Frame Extraction**?\n'
                       '109. What problem does **Temporal Segment Extraction** solve in a '
                       'multimodal RAG system?\n'
                       '110. What information could be lost if **Temporal Segment Extraction** is '
                       'implemented poorly?\n'
                       '111. What production trade-off or validation check is most important for '
                       '**Temporal Segment Extraction**?\n'
                       '112. What problem does **Keyframe Extraction** solve in a multimodal RAG '
                       'system?\n'
                       '113. What information could be lost if **Keyframe Extraction** is '
                       'implemented poorly?\n'
                       '114. What production trade-off or validation check is most important for '
                       '**Keyframe Extraction**?\n'
                       '115. What problem does **Choosing a Video Extraction Strategy** solve in a '
                       'multimodal RAG system?\n'
                       '116. What information could be lost if **Choosing a Video Extraction '
                       'Strategy** is implemented poorly?\n'
                       '117. What production trade-off or validation check is most important for '
                       '**Choosing a Video Extraction Strategy**?\n'
                       '118. What problem does **Computational Economics and Latency** solve in a '
                       'multimodal RAG system?\n'
                       '119. What information could be lost if **Computational Economics and '
                       'Latency** is implemented poorly?\n'
                       '120. What production trade-off or validation check is most important for '
                       '**Computational Economics and Latency**?\n'
                       '121. What problem does **Modality Alignment** solve in a multimodal RAG '
                       'system?\n'
                       '122. What information could be lost if **Modality Alignment** is '
                       'implemented poorly?\n'
                       '123. What production trade-off or validation check is most important for '
                       '**Modality Alignment**?\n'
                       '124. What problem does **The Interface Layer: Visual Citations** solve in '
                       'a multimodal RAG system?\n'
                       '125. What information could be lost if **The Interface Layer: Visual '
                       'Citations** is implemented poorly?\n'
                       '126. What production trade-off or validation check is most important for '
                       '**The Interface Layer: Visual Citations**?\n'
                       '127. What problem does **Security, Privacy, and Governance** solve in a '
                       'multimodal RAG system?\n'
                       '128. What information could be lost if **Security, Privacy, and '
                       'Governance** is implemented poorly?\n'
                       '129. What production trade-off or validation check is most important for '
                       '**Security, Privacy, and Governance**?\n'
                       '130. What problem does **Visual Prompt Injection** solve in a multimodal '
                       'RAG system?\n'
                       '131. What information could be lost if **Visual Prompt Injection** is '
                       'implemented poorly?\n'
                       '132. What production trade-off or validation check is most important for '
                       '**Visual Prompt Injection**?\n'
                       '133. What problem does **Unstructured PII Leakage** solve in a multimodal '
                       'RAG system?\n'
                       '134. What information could be lost if **Unstructured PII Leakage** is '
                       'implemented poorly?\n'
                       '135. What production trade-off or validation check is most important for '
                       '**Unstructured PII Leakage**?\n'
                       '136. What problem does **Deep Observability for Multimodal Pipelines** '
                       'solve in a multimodal RAG system?\n'
                       '137. What information could be lost if **Deep Observability for Multimodal '
                       'Pipelines** is implemented poorly?\n'
                       '138. What production trade-off or validation check is most important for '
                       '**Deep Observability for Multimodal Pipelines**?\n'
                       '139. What problem does **How Multimodal Hallucinations Arise** solve in a '
                       'multimodal RAG system?\n'
                       '140. What information could be lost if **How Multimodal Hallucinations '
                       'Arise** is implemented poorly?\n'
                       '141. What production trade-off or validation check is most important for '
                       '**How Multimodal Hallucinations Arise**?\n'
                       '142. What problem does **Detecting Multimodal Hallucinations** solve in a '
                       'multimodal RAG system?\n'
                       '143. What information could be lost if **Detecting Multimodal '
                       'Hallucinations** is implemented poorly?\n'
                       '144. What production trade-off or validation check is most important for '
                       '**Detecting Multimodal Hallucinations**?\n'
                       '145. What is the core difference between the conversion and native '
                       'multimodal approaches?\n'
                       '146. Why is preserving provenance as important as preserving content?\n'
                       '147. Why can a system be faithful to a bad image summary and still be '
                       'wrong?\n'
                       '148. When should retrieval use a compressed representation but generation '
                       'use the original object?\n'
                       '149. How would you evaluate a pipeline that supports text, tables, images, '
                       'audio, and video?\n'
                       '150. What single design principle connects table stitching, image '
                       'dereferencing, timestamps, and visual citations?\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Final takeaway\n'
                       '\n'
                       'Multimodal RAG succeeds when every transformation preserves enough meaning '
                       'and provenance for the next stage. Use the cheapest searchable '
                       'representation that preserves recall, keep a path back to the original '
                       'evidence, and escalate to richer multimodal reasoning only when the '
                       'question requires it.\n',
            'estimated_minutes': 690,
            'has_code_examples': True,
            'has_manual_image_requests': True,
            'sections': [{'id': 'why-multimodal-rag-matters',
                          'title': 'Why Multimodal RAG Matters',
                          'order': 1},
                         {'id': 'conversion-vs-native',
                          'title': 'Conversion Versus Native Multimodal RAG',
                          'order': 2},
                         {'id': 'multimodal-design-principle',
                          'title': 'Design Principle: Preserve Semantics, Not Just Bytes',
                          'order': 3},
                         {'id': 'tables-as-semantic-documents',
                          'title': 'Tables as Semantic Micro-Documents',
                          'order': 4},
                         {'id': 'table-extraction-three-stages',
                          'title': 'The Three Stages of Table Extraction',
                          'order': 5},
                         {'id': 'table-tools',
                          'title': 'Choosing Table Extraction Tools',
                          'order': 6},
                         {'id': 'docling-example',
                          'title': 'Table Extraction with Docling: What the Example Teaches',
                          'order': 7},
                         {'id': 'parser-failure-is-normal',
                          'title': 'Parser Failure Is Normal—Design for It',
                          'order': 8},
                         {'id': 'conditional-table-routing',
                          'title': 'Conditional Parsing Pipelines',
                          'order': 9},
                         {'id': 'naive-table-chunking',
                          'title': 'Why Naive Chunking Breaks Tables',
                          'order': 10},
                         {'id': 'structured-table-representation',
                          'title': 'Represent Tables as Structured Context',
                          'order': 11},
                         {'id': 'summary-pointer-pattern',
                          'title': 'The Summary-Pointer Pattern for Tables',
                          'order': 12},
                         {'id': 'mixed-context-prompts',
                          'title': 'Prompting with Mixed Text and Structured Data',
                          'order': 13},
                         {'id': 'multi-page-tables',
                          'title': 'Why Multi-Page Tables Are a Special Case',
                          'order': 14},
                         {'id': 'table-stitching',
                          'title': 'A Practical Table-Stitching Heuristic',
                          'order': 15},
                         {'id': 'table-rag-flow',
                          'title': 'End-to-End Table RAG Flow',
                          'order': 16},
                         {'id': 'images-why-text-extraction-is-insufficient',
                          'title': 'Why Images Need More Than OCR',
                          'order': 17},
                         {'id': 'image-strategy-choice',
                          'title': 'Two Main Image Strategies',
                          'order': 18},
                         {'id': 'image-summarization',
                          'title': 'Image Summarization During Ingestion',
                          'order': 19},
                         {'id': 'image-summary-loss',
                          'title': 'The Information Bottleneck of Image Summaries',
                          'order': 20},
                         {'id': 'summary-plus-original-image',
                          'title': 'Retrieve by Summary, Reason over the Original Image',
                          'order': 21},
                         {'id': 'text-only-vs-summary-vs-raw-image',
                          'title': 'Three Levels of Visual Fidelity',
                          'order': 22},
                         {'id': 'shared-embedding-space',
                          'title': 'Shared Text–Image Embedding Spaces',
                          'order': 23},
                         {'id': 'contrastive-learning-intuition',
                          'title': 'Contrastive Learning Intuition',
                          'order': 24},
                         {'id': 'siglip-retrieval',
                          'title': 'SigLIP Retrieval: What the Example Demonstrates',
                          'order': 25},
                         {'id': 'shared-embedding-strengths',
                          'title': 'Where Shared Embeddings Shine',
                          'order': 26},
                         {'id': 'shared-embedding-limitations',
                          'title': 'Where Shared Embeddings Struggle',
                          'order': 27},
                         {'id': 'hybrid-multimodal-design',
                          'title': 'Hybrid Multimodal Architectures',
                          'order': 28},
                         {'id': 'audio-video-overview',
                          'title': 'Audio and Video as RAG Knowledge Sources',
                          'order': 29},
                         {'id': 'asr-baseline',
                          'title': 'High-Fidelity ASR as the Baseline',
                          'order': 30},
                         {'id': 'speaker-diarization',
                          'title': 'Why Speaker Diarization Matters',
                          'order': 31},
                         {'id': 'transcript-chunking',
                          'title': 'Chunking Transcripts Without Losing Dialogue Structure',
                          'order': 32},
                         {'id': 'deepgram-example',
                          'title': 'ASR Pipeline Example: Lessons from Deepgram',
                          'order': 33},
                         {'id': 'jump-to-source',
                          'title': 'Designing Jump-to-Source Multimedia UX',
                          'order': 34},
                         {'id': 'red-button-problem',
                          'title': 'The Red-Button Problem',
                          'order': 35},
                         {'id': 'fixed-frame-extraction',
                          'title': 'Fixed-Interval Frame Extraction',
                          'order': 36},
                         {'id': 'temporal-segment-extraction',
                          'title': 'Temporal Segment Extraction',
                          'order': 37},
                         {'id': 'keyframe-extraction', 'title': 'Keyframe Extraction', 'order': 38},
                         {'id': 'video-strategy-tradeoffs',
                          'title': 'Choosing a Video Extraction Strategy',
                          'order': 39},
                         {'id': 'multimodal-cost-latency',
                          'title': 'Computational Economics and Latency',
                          'order': 40},
                         {'id': 'modality-alignment', 'title': 'Modality Alignment', 'order': 41},
                         {'id': 'visual-citations',
                          'title': 'The Interface Layer: Visual Citations',
                          'order': 42},
                         {'id': 'security-privacy',
                          'title': 'Security, Privacy, and Governance',
                          'order': 43},
                         {'id': 'visual-prompt-injection',
                          'title': 'Visual Prompt Injection',
                          'order': 44},
                         {'id': 'unstructured-pii',
                          'title': 'Unstructured PII Leakage',
                          'order': 45},
                         {'id': 'multimodal-observability',
                          'title': 'Deep Observability for Multimodal Pipelines',
                          'order': 46},
                         {'id': 'multimodal-hallucinations',
                          'title': 'How Multimodal Hallucinations Arise',
                          'order': 47},
                         {'id': 'detecting-multimodal-hallucinations',
                          'title': 'Detecting Multimodal Hallucinations',
                          'order': 48},
                         {'id': 'multimodal-retrieval-evaluation',
                          'title': 'Evaluating Multimodal Retrieval',
                          'order': 49},
                         {'id': 'vlm-as-judge',
                          'title': 'Evaluating Generation with a VLM-as-a-Judge',
                          'order': 50},
                         {'id': 'end-to-end-multimodal-evaluation',
                          'title': 'Build Evaluation at Every Representation Boundary',
                          'order': 51},
                         {'id': 'table-architecture-decision',
                          'title': 'Decision Guide for Table Architectures',
                          'order': 52},
                         {'id': 'image-architecture-decision',
                          'title': 'Decision Guide for Image Architectures',
                          'order': 53},
                         {'id': 'audio-video-architecture-decision',
                          'title': 'Decision Guide for Audio and Video Architectures',
                          'order': 54},
                         {'id': 'production-blueprint',
                          'title': 'A Production Multimodal RAG Blueprint',
                          'order': 55},
                         {'id': 'common-mistakes',
                          'title': 'Common Multimodal RAG Mistakes',
                          'order': 56},
                         {'id': 'terminology',
                          'title': 'Terminology You Should Retain',
                          'order': 57},
                         {'id': 'retain-this-idea',
                          'title': 'Retain This Mental Model',
                          'order': 58}]},
 'exercises': [{'id': 'M01.L08.EX01',
                'title': 'Choose Conversion or Native',
                'lesson_code': 'M01.L08',
                'section_id': 'conversion-vs-native',
                'placement': 'after_section',
                'description': 'Given three workloads—financial tables, product-photo search, and '
                               'a scanned manual—choose conversion, native multimodal retrieval, '
                               'or a hybrid approach for each and justify the decision.',
                'instructions': ('1. For each workload, identify the dominant information-bearing modality, decide where conversion would lose meaning, and choose conversion, native retrieval, or a hybrid.\n'
                                 '2. Include one operational reason for each choice.'),
                'expected_output': 'A three-row decision table with workload, chosen architecture, '
                                   'information-loss risk, and operational rationale.',
                'skill_tested': ['architecture', 'multimodal-rag'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX02',
                'title': 'Diagnose a Table Failure',
                'lesson_code': 'M01.L08',
                'section_id': 'table-extraction-three-stages',
                'placement': 'after_section',
                'description': 'A parser returns correct characters but places values under the '
                               'wrong columns. Identify which extraction stage failed and propose '
                               'two validation checks.',
                'instructions': ('1. Trace the failure through table detection, cell OCR/reading, and normalization.\n'
                                 '2. Then propose two automated checks that would catch column misalignment before indexing.'),
                'expected_output': 'A stage-level diagnosis plus two concrete validation rules, '
                                   'such as header/value type checks or row/column consistency '
                                   'checks.',
                'skill_tested': ['table-extraction', 'validation'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX03',
                'title': 'Build a Parser Evaluation Harness',
                'lesson_code': 'M01.L08',
                'section_id': 'parser-failure-is-normal',
                'placement': 'after_section',
                'description': 'Design a small representative test corpus and define structural '
                               'checks you would use to compare two table parsers.',
                'instructions': ('1. Select 8–12 representative documents with easy, merged-cell, borderless, rotated, and scanned tables.\n'
                                 '2. Define the expected structure manually, then compare two parsers on extraction completeness and structural accuracy.'),
                'expected_output': 'A small parser benchmark specification with document '
                                   'categories, expected outputs, scoring criteria, and a '
                                   'parser-selection rule.',
                'skill_tested': ['table-parsing', 'evaluation'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX04',
                'title': 'Repair Headless Table Chunks',
                'lesson_code': 'M01.L08',
                'section_id': 'naive-table-chunking',
                'placement': 'after_section',
                'description': 'Explain why a retrieved table row without headers is unsafe, then '
                               'redesign the representation so the row retains schema context.',
                'instructions': ('1. Rewrite the headless row into a representation that preserves its column names and units.\n'
                                 '2. Explain why the new representation is safer for both retrieval and generation.'),
                'expected_output': 'A repaired structured row plus a short explanation of how '
                                   'schema context prevents value misinterpretation.',
                'skill_tested': ['table-chunking', 'structured-context'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX05',
                'title': 'Design a Table Summary Pointer',
                'lesson_code': 'M01.L08',
                'section_id': 'summary-pointer-pattern',
                'placement': 'after_section',
                'description': 'Describe the metadata required to retrieve a table summary and '
                               'dereference the authoritative full table at generation time.',
                'instructions': ('1. Define the summary chunk, authoritative table object, stable table ID, source page, bounding box, schema, and storage pointer.\n'
                                 '2. Show how a query-time match to the summary resolves back to the full table.'),
                'expected_output': 'A metadata schema and a 4–6 step dereference flow from '
                                   'retrieved summary to authoritative table context.',
                'skill_tested': ['table-rag', 'provenance'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX06',
                'title': 'Stitch a Multi-Page Table',
                'lesson_code': 'M01.L08',
                'section_id': 'multi-page-tables',
                'placement': 'after_section',
                'description': 'Define at least four signals you would require before merging two '
                               'adjacent page-level table fragments.',
                'instructions': ('1. Define merge requirements using page adjacency, identical or compatible column count, header similarity, data-type compatibility, table title continuity, and repeated-header handling.\n'
                                 '2. State when the merge must be rejected.'),
                'expected_output': 'A table-stitching checklist with positive merge signals and at '
                                   'least two rejection conditions.',
                'skill_tested': ['table-stitching', 'document-parsing'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX07',
                'title': 'Write an Image Summary Contract',
                'lesson_code': 'M01.L08',
                'section_id': 'image-summarization',
                'placement': 'after_section',
                'description': 'Draft the fields a VLM-generated image summary should capture for '
                               'a chart so future queries can retrieve it reliably.',
                'instructions': ('1. Write a chart-summary contract that captures chart type, title, axes, units, legends, major values, trends, anomalies, and uncertainty.\n'
                                 '2. Separate facts visible in the image from interpretations.'),
                'expected_output': 'A structured image-summary template that could be indexed as '
                                   'retrieval text without losing critical chart semantics.',
                'skill_tested': ['image-summarization', 'vlm'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX08',
                'title': 'Design Two-Tier Image RAG',
                'lesson_code': 'M01.L08',
                'section_id': 'summary-plus-original-image',
                'placement': 'after_section',
                'description': 'Sketch the ingestion and query flow for retrieving by image '
                               'summary but reasoning over the original image.',
                'instructions': ('1. Draw the ingestion path from image extraction to VLM summary to vector index while storing the original image separately.\n'
                                 '2. Then draw the query path that retrieves by summary and supplies the raw image to a VLM only when needed.'),
                'expected_output': 'An ingestion/query sequence with summary embedding, '
                                   'source-image pointer, retrieval, dereferencing, and final '
                                   'multimodal generation.',
                'skill_tested': ['image-rag', 'multimodal-generation'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX09',
                'title': 'Cross-Modal Retrieval Walkthrough',
                'lesson_code': 'M01.L08',
                'section_id': 'shared-embedding-space',
                'placement': 'after_section',
                'description': 'Explain how a text query can retrieve an image with no text '
                               'metadata when both are encoded into a shared vector space.',
                'instructions': ('1. Walk through image encoding, text-query encoding, vector normalization, cosine/dot-product similarity, and top-k selection.\n'
                                 '2. Explain why no filename or caption is required for the match.'),
                'expected_output': 'A five-step cross-modal retrieval explanation using the shared '
                                   'latent-space mental model.',
                'skill_tested': ['multimodal-embeddings', 'retrieval'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX10',
                'title': 'Choose the Right Visual Representation',
                'lesson_code': 'M01.L08',
                'section_id': 'shared-embedding-limitations',
                'placement': 'after_section',
                'description': 'For a product catalog, a financial chart, and an engineering '
                               'schematic, decide whether shared embeddings alone are sufficient.',
                'instructions': ('1. For each workload, judge whether coarse visual similarity is enough or whether exact visual reasoning is required.\n'
                                 '2. Add the fallback representation you would use when shared embeddings are insufficient.'),
                'expected_output': 'Three architecture decisions that distinguish visual-search '
                                   'workloads from information-dense visual reasoning workloads.',
                'skill_tested': ['visual-retrieval', 'architecture'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX11',
                'title': 'Make Audio Evidence Attributable',
                'lesson_code': 'M01.L08',
                'section_id': 'speaker-diarization',
                'placement': 'after_section',
                'description': 'Define the minimum metadata fields for transcript chunks that '
                               'support speaker filtering and jump-to-source playback.',
                'instructions': ('1. Define transcript chunk metadata for source recording ID, speaker IDs, start/end timestamps, language, confidence, and permissions.\n'
                                 '2. Explain how each field supports retrieval or verification.'),
                'expected_output': 'A transcript-chunk schema sufficient for speaker filtering, '
                                   'source playback, auditing, and permission enforcement.',
                'skill_tested': ['asr', 'diarization'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX12',
                'title': 'Recover Silent Video Semantics',
                'lesson_code': 'M01.L08',
                'section_id': 'red-button-problem',
                'placement': 'after_section',
                'description': 'Design a representation for a training video where the spoken '
                               "instruction is ambiguous without seeing the operator's action.",
                'instructions': ('1. Represent the same video moment with transcript text, timestamp, visual caption/keyframe, and source-video ID.\n'
                                 '2. Explain how the visual record resolves the ambiguous spoken phrase.'),
                'expected_output': 'A multimodal evidence object that links the spoken instruction '
                                   'to the visual action and exact playback location.',
                'skill_tested': ['video-rag', 'multimodal-context'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX13',
                'title': 'Select a Video Sampling Strategy',
                'lesson_code': 'M01.L08',
                'section_id': 'video-strategy-tradeoffs',
                'placement': 'after_section',
                'description': 'Choose fixed frames, temporal segments, keyframes, or a hybrid '
                               'strategy for three different video workloads and explain why.',
                'instructions': ('1. Choose a sampling strategy for a security-camera stream, a repair tutorial, and a product-demo video.\n'
                                 '2. Compare granularity, temporal reasoning, ingestion cost, and storage.'),
                'expected_output': 'A three-row comparison with selected strategy and explicit '
                                   'quality/cost trade-offs.',
                'skill_tested': ['video-rag', 'sampling'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX14',
                'title': 'Control Multimodal Cost',
                'lesson_code': 'M01.L08',
                'section_id': 'multimodal-cost-latency',
                'placement': 'after_section',
                'description': 'Identify which expensive transformations can be moved to ingestion '
                               'time and which must remain query-time for high-fidelity answers.',
                'instructions': ('1. Separate transformations that can be cached at ingestion—OCR, ASR, summaries, embeddings—from query-time work such as raw-image inspection for high-fidelity questions.\n'
                                 '2. Explain one case where query-time multimodal reasoning is unavoidable.'),
                'expected_output': 'A two-column ingestion-vs-query cost plan with a justification '
                                   'for the expensive query-time path.',
                'skill_tested': ['multimodal-rag', 'cost'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX15',
                'title': 'Threat-Model a Visual Injection',
                'lesson_code': 'M01.L08',
                'section_id': 'visual-prompt-injection',
                'placement': 'after_section',
                'description': 'Describe how malicious text hidden inside an image could influence '
                               'a VLM and propose a layered defense.',
                'instructions': ('1. Describe the attack path from hidden visual instruction to VLM behavior.\n'
                                 '2. Add controls at ingestion, retrieval, prompt construction, and tool/action layers, and state which control limits impact if earlier defenses fail.'),
                'expected_output': 'A layered visual-prompt-injection threat model with preventive '
                                   'and containment controls.',
                'skill_tested': ['security', 'visual-prompt-injection'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX16',
                'title': 'Trace a Hallucination to Its Source',
                'lesson_code': 'M01.L08',
                'section_id': 'multimodal-hallucinations',
                'placement': 'after_section',
                'description': 'Given a wrong chart-based answer, list checks that distinguish OCR '
                               'error, summary error, retrieval error, and generation error.',
                'instructions': ('1. Start from the wrong answer and inspect, in order, source image quality, OCR/table extraction, generated summary, retrieval ranking, original-image dereference, and VLM answer.\n'
                                 '2. Record the evidence that would confirm each failure class.'),
                'expected_output': 'A debugging decision tree that distinguishes representation, '
                                   'retrieval, alignment, and generation failures.',
                'skill_tested': ['observability', 'multimodal-hallucinations'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX17',
                'title': 'Design a Multimodal Recall Test',
                'lesson_code': 'M01.L08',
                'section_id': 'multimodal-retrieval-evaluation',
                'placement': 'after_section',
                'description': 'Create an evaluation query set in which some answers depend only '
                               'on tables, some only on images, and some on video.',
                'instructions': ('1. Create at least nine evaluation cases: three table-dependent, three image-dependent, and three audio/video-dependent.\n'
                                 '2. For each, identify the golden artifact and define recall@k success.'),
                'expected_output': 'A modality-balanced retrieval benchmark with query, required '
                                   'evidence artifact, and pass/fail retrieval criterion.',
                'skill_tested': ['evaluation', 'multimodal-retrieval'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L08.EX18',
                'title': 'Architect a Multimodal RAG Service',
                'lesson_code': 'M01.L08',
                'section_id': 'production-blueprint',
                'placement': 'after_section',
                'description': 'Draw or describe a production architecture with separate modality '
                               'processors, shared retrieval, provenance, and evaluation.',
                'instructions': ('1. Design separate ingestion workers for text, tables, images, and audio/video.\n'
                                 '2. Specify the shared IDs and the storage every worker writes to.\n'
                                 '3. Describe indexing and how retrieval results from all modalities are fused.\n'
                                 '4. Show how an answer dereferences back to its sources.\n'
                                 '5. Add the tracing, security and evaluation services.'),
                'expected_output': 'An end-to-end production architecture with modality '
                                   'processors, shared provenance, retrieval, generation, '
                                   'observability, and evaluation boundaries.',
                'skill_tested': ['architecture', 'production-multimodal-rag'],
                'difficulty': 'intermediate'}],
 'quiz': {'id': 'M01.L08.QUIZ',
          'title': 'Multimodal RAG — Lesson Quiz',
          'lesson_code': 'M01.L08',
          'placement': 'lesson_end',
          'questions': [{'id': 'M01.L08.Q01',
                         'type': 'multiple_choice',
                         'section_id': 'conversion-vs-native',
                         'question': 'Which statement best distinguishes the conversion approach '
                                     'from a native multimodal approach?',
                         'options': ['Conversion transforms non-text data into text/structured '
                                     'representations for a standard RAG stack',
                                     'Conversion requires only image embeddings',
                                     'Native multimodal RAG cannot use text',
                                     'Native multimodal RAG always has lower latency'],
                         'correct': 0,
                         'explanation': 'Conversion deliberately translates non-text evidence into '
                                        'representations that conventional RAG components can '
                                        'process.'},
                        {'id': 'M01.L08.Q02',
                         'type': 'multiple_choice',
                         'section_id': 'table-extraction-three-stages',
                         'question': 'What should happen before interpreting cell text in a '
                                     'complex table?',
                         'options': ['Generate embeddings',
                                     'Recover the table structure and cell boundaries',
                                     'Run reranking',
                                     'Summarize the entire PDF'],
                         'correct': 1,
                         'explanation': 'If row/column boundaries are wrong, even perfect OCR '
                                        'produces semantically jumbled data.'},
                        {'id': 'M01.L08.Q03',
                         'type': 'multiple_choice',
                         'section_id': 'naive-table-chunking',
                         'question': 'Why can ordinary text chunking make a table row unsafe to '
                                     'retrieve?',
                         'options': ['Rows become encrypted',
                                     'Headers can be separated from values',
                                     'Vector databases reject Markdown',
                                     'LLMs cannot parse numbers'],
                         'correct': 1,
                         'explanation': 'The key failure is loss of schema context: the model sees '
                                        'values without their column meanings.'},
                        {'id': 'M01.L08.Q04',
                         'type': 'multiple_choice',
                         'section_id': 'summary-pointer-pattern',
                         'question': 'What is the main purpose of a table summary in the '
                                     'summary-pointer pattern?',
                         'options': ['Replace the full table permanently',
                                     'Provide a compact searchable representation that points to '
                                     'the full table',
                                     'Normalize every numeric value',
                                     'Eliminate metadata'],
                         'correct': 1,
                         'explanation': 'The summary helps retrieval while the full structured '
                                        'object remains authoritative for generation.'},
                        {'id': 'M01.L08.Q05',
                         'type': 'multiple_choice',
                         'section_id': 'multi-page-tables',
                         'question': 'What is a major risk when stitching multi-page table '
                                     'fragments using only column count?',
                         'options': ['The vector dimension changes',
                                     'Unrelated tables with the same width may be merged',
                                     'OCR stops working',
                                     'Headers cannot repeat'],
                         'correct': 1,
                         'explanation': 'Column count is a weak signal; page adjacency, headers, '
                                        'types, and titles provide stronger evidence.'},
                        {'id': 'M01.L08.Q06',
                         'type': 'multiple_choice',
                         'section_id': 'image-summarization',
                         'question': 'What is the central weakness of image summarization?',
                         'options': ['It cannot be embedded',
                                     'It is a lossy representation and may omit details needed by '
                                     'later queries',
                                     'It requires no storage',
                                     'It prevents text retrieval'],
                         'correct': 1,
                         'explanation': 'Once an omitted detail is lost from the summary, later '
                                        'text-only generation cannot recover it.'},
                        {'id': 'M01.L08.Q07',
                         'type': 'multiple_choice',
                         'section_id': 'summary-plus-original-image',
                         'question': 'Why retrieve by summary but generate with the original '
                                     'image?',
                         'options': ['To avoid provenance',
                                     'To combine efficient text retrieval with higher-fidelity '
                                     'visual reasoning',
                                     'To remove the need for embeddings',
                                     'To prevent citations'],
                         'correct': 1,
                         'explanation': 'This two-tier pattern separates search efficiency from '
                                        'reasoning fidelity.'},
                        {'id': 'M01.L08.Q08',
                         'type': 'multiple_choice',
                         'section_id': 'shared-embedding-space',
                         'question': 'How can a text query retrieve an uncaptioned image in a '
                                     'shared embedding model?',
                         'options': ['OCR is mandatory',
                                     'Text and image encoders map both inputs into a comparable '
                                     'latent space',
                                     'The image is converted to SQL',
                                     'The query is matched by BM25'],
                         'correct': 1,
                         'explanation': 'Cross-modal similarity works because semantically related '
                                        'representations are close in the same space.'},
                        {'id': 'M01.L08.Q09',
                         'type': 'multiple_choice',
                         'section_id': 'shared-embedding-limitations',
                         'question': 'Why may shared visual embeddings underperform on dense '
                                     'charts?',
                         'options': ['Charts contain no pixels',
                                     'A single semantic vector may not preserve exact values and '
                                     'fine relationships',
                                     'Cosine similarity cannot compare vectors',
                                     'Images cannot be indexed'],
                         'correct': 1,
                         'explanation': 'These models are optimized for semantic alignment, not '
                                        'perfect preservation of every visual fact.'},
                        {'id': 'M01.L08.Q10',
                         'type': 'multiple_choice',
                         'section_id': 'speaker-diarization',
                         'question': 'What does speaker diarization add to an audio transcript?',
                         'options': ['Image metadata',
                                     'Who spoke when',
                                     'Higher vector dimensions',
                                     'Table headers'],
                         'correct': 1,
                         'explanation': 'Diarization turns a flat transcript into attributable '
                                        'evidence.'},
                        {'id': 'M01.L08.Q11',
                         'type': 'multiple_choice',
                         'section_id': 'red-button-problem',
                         'question': 'Why does transcription alone fail in the red-button example?',
                         'options': ['The audio file is too short',
                                     'The spoken phrase depends on a visual referent not present '
                                     'in the words',
                                     'ASR cannot process verbs',
                                     'The video has no timestamps'],
                         'correct': 1,
                         'explanation': "The meaning of 'this' lives in the visual action."},
                        {'id': 'M01.L08.Q12',
                         'type': 'multiple_choice',
                         'section_id': 'video-strategy-tradeoffs',
                         'question': 'Which strategy best captures actions unfolding across time?',
                         'options': ['Single fixed frames only',
                                     'Temporal segment extraction',
                                     'BM25',
                                     'Table stitching'],
                         'correct': 1,
                         'explanation': 'Temporal segments let a VLM observe sequences rather than '
                                        'isolated images.'},
                        {'id': 'M01.L08.Q13',
                         'type': 'multiple_choice',
                         'section_id': 'visual-citations',
                         'question': 'What is the main value of visual or timestamp citations?',
                         'options': ['They reduce embedding dimensions',
                                     'They let users inspect the original evidence directly',
                                     'They replace evaluation',
                                     'They eliminate storage'],
                         'correct': 1,
                         'explanation': 'Multimodal citations reduce verification cost and improve '
                                        'trust.'},
                        {'id': 'M01.L08.Q14',
                         'type': 'multiple_choice',
                         'section_id': 'visual-prompt-injection',
                         'question': 'How should text extracted from an image be treated?',
                         'options': ['As trusted system instructions',
                                     'As untrusted content that may contain indirect prompt '
                                     'injection',
                                     'As a database key only',
                                     'As impossible to attack'],
                         'correct': 1,
                         'explanation': 'Visual content can contain malicious instructions just '
                                        'like retrieved text.'},
                        {'id': 'M01.L08.Q15',
                         'type': 'multiple_choice',
                         'section_id': 'multimodal-hallucinations',
                         'question': 'Why is final-answer faithfulness to an image summary not '
                                     'sufficient?',
                         'options': ['Summaries cannot be stored',
                                     'The summary itself may be wrong or incomplete relative to '
                                     'the original image',
                                     'LLMs cannot read summaries',
                                     'Retrieval always fails'],
                         'correct': 1,
                         'explanation': 'Evaluation must sometimes compare against the original '
                                        'modality, not only a derived representation.'},
                        {'id': 'M01.L08.Q16',
                         'type': 'multiple_choice',
                         'section_id': 'multimodal-retrieval-evaluation',
                         'question': 'What should a multimodal retrieval benchmark contain?',
                         'options': ['Only text-answerable queries',
                                     'Queries that genuinely require each supported modality',
                                     'Only synthetic images',
                                     'Only latency tests'],
                         'correct': 1,
                         'explanation': 'Otherwise the benchmark may never test whether multimodal '
                                        'retrieval actually works.'},
                        {'id': 'M01.L08.Q17',
                         'type': 'multiple_choice',
                         'section_id': 'production-blueprint',
                         'question': 'Which design best supports debugging a multimodal pipeline?',
                         'options': ['One opaque script',
                                     'Separate modality processors with stable provenance and '
                                     'tracing across transformations',
                                     'Discarding intermediate representations',
                                     'Removing metadata'],
                         'correct': 1,
                         'explanation': 'Modularity and provenance make it possible to localize '
                                        'failures.'},
                        {'id': 'M01.L08.Q18',
                         'type': 'multiple_choice',
                         'section_id': 'retain-this-idea',
                         'question': 'Which principle best summarizes this lesson?',
                         'options': ['Always convert everything to text',
                                     'Retrieve with an efficient representation, reason with the '
                                     'fidelity required, and cite the original evidence',
                                     'Always use the most expensive VLM',
                                     'Store only embeddings'],
                         'correct': 1,
                         'explanation': 'The core design principle is to balance search efficiency '
                                        'with evidence fidelity and verifiability.'}],
          'passing_score': 70}}
