"""M01.L09 — Knowledge-Enhanced RAG.

One Topic -> one complete learner-facing Lesson + inline Images + inline Exercises + lesson Quiz.
Supplied source, Chapter 9, pages not provided.
Instructor-authored curriculum adaptation.
"""

from app.models.learning import DifficultyLevel

LESSON_CODE = "M01.L09"
MODULE_ORDER = 1
MODULE_TITLE = 'RAG Foundations'
MODULE_DESCRIPTION = 'Build, evaluate, operate, and extend RAG systems from semantic retrieval through agents, multimodal evidence, and knowledge-enhanced architectures.'
SOURCE_CHAPTER = 9
SOURCE_PAGES = "Not provided in supplied source"

TOPIC = {'title': 'Knowledge-Enhanced RAG',
 'slug': 'rag-foundations-m01-l09',
 'description': 'A study-ready guide to knowledge graphs, graph query languages, chunk enrichment, '
                'hybrid graph retrieval, entity linking, GraphRAG, graph infrastructure, '
                'incremental updates, and the accuracy-versus-cost trade-off.',
 'order': 9,
 'difficulty': 'intermediate',
 'estimated_hours': 11.5,
 'skill_tags': ['rag',
                'knowledge-graphs',
                'graph-rag',
                'graphrag',
                'cypher',
                'sparql',
                'neo4j',
                'entity-linking',
                'ontology',
                'schema',
                'graph-retrieval',
                'hybrid-retrieval',
                'graph-infrastructure',
                'cdc',
                'evaluation',
                'module-01'],
 'prerequisite_ids': ['M01.L01',
                      'M01.L02',
                      'M01.L03',
                      'M01.L04',
                      'M01.L05',
                      'M01.L06',
                      'M01.L07',
                      'M01.L08'],
 'lesson': {'title': 'Knowledge-Enhanced RAG',
            'content': '# Knowledge-Enhanced RAG\n'
                       '\n'
                       '> **Course:** Retrieval-Augmented Generation (RAG)  \n'
                       '> **Lesson:** M01.L09  \n'
                       '> **Module:** RAG Foundations  \n'
                       '> **Source alignment:** Supplied source, Chapter 9. Page numbers were not '
                       'provided. This lesson is an instructor-authored study adaptation rather '
                       'than a reproduction of the source text.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Learning outcomes\n'
                       '\n'
                       'By the end of this lesson, you should be able to:\n'
                       '\n'
                       '- Explain why semantic and hybrid retrieval struggle with time-bound, '
                       'multi-constraint, and multi-hop questions.\n'
                       '- Model knowledge using entities, properties, and typed relationships.\n'
                       '- Read basic Cypher and SPARQL graph-query patterns.\n'
                       '- Distinguish an ontology from a concrete graph schema.\n'
                       '- Explain how text chunks and domain entities can coexist in one knowledge '
                       'graph.\n'
                       '- Compare chunk enrichment with hybrid graph retrieval.\n'
                       '- Design a guarded natural-language-to-Cypher query path.\n'
                       '- Decide whether vectors belong inside the graph database or in a separate '
                       'vector store.\n'
                       '- Explain entity extraction, relation extraction, entity linking, and '
                       'canonicalization.\n'
                       '- Use standard ontologies or curated knowledge graphs to reduce '
                       'graph-construction effort.\n'
                       '- Explain Microsoft GraphRAG, community detection, and local versus global '
                       'search.\n'
                       '- Identify when GraphRAG is too expensive or too lossy for the use case.\n'
                       '- Design idempotent KG ingestion, schema evolution, incremental updates, '
                       'and entity merges.\n'
                       '- Evaluate the accuracy, latency, cost, and operational burden of '
                       'knowledge-enhanced RAG.\n'
                       '- Use RAG evaluation failures to decide whether a knowledge graph is '
                       'justified.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '\n'
                       '## 1. Why Knowledge-Enhanced RAG Exists\n'
                       '\n'
                       'Vector and hybrid retrieval are excellent at finding semantically similar '
                       'text, but similarity is not the same thing as a verified relationship. A '
                       'query can be topically close to many passages and still require an answer '
                       'that depends on an exact date, the intersection of several constraints, or '
                       'a chain of relationships across multiple entities.\n'
                       '\n'
                       'Knowledge-enhanced RAG adds an explicit relationship layer. Instead of '
                       'asking only, “Which chunks look similar to this query?”, the system can '
                       'also ask, “Which entities are connected by the exact relations needed to '
                       'answer it?” This changes retrieval from purely probabilistic matching '
                       'toward structured factual traversal.\n'
                       '\n'
                       'The lesson’s central architectural idea is not that graphs replace RAG. '
                       'Graphs complement semantic retrieval when relationships, constraints, and '
                       'multi-hop logic matter enough to justify their operational cost.\n'
                       '\n'
                       '\n'
                       '## 2. Failure Mode 1: Time-Bound Facts\n'
                       '\n'
                       'Embeddings compress meaning, but they do not automatically understand '
                       'which fact was true at a specific point in time. A corpus can contain '
                       'several historically correct statements about the same entity. Semantic '
                       'search may retrieve all of them because they are conceptually similar.\n'
                       '\n'
                       'For time-sensitive questions, the important information is not only the '
                       'entity but the validity interval of a fact. A graph can model this '
                       'explicitly by attaching temporal properties to nodes or relationships, or '
                       'by maintaining historically distinct relationships.\n'
                       '\n'
                       'The engineering lesson is that dates are not decoration. If the '
                       'application must answer “who held role X at date Y?”, the data model must '
                       'represent time in a queryable way.\n'
                       '\n'
                       '\n'
                       '## 3. Failure Mode 2: Intersections of Constraints\n'
                       '\n'
                       'A user may ask for entities satisfying several conditions simultaneously. '
                       'Vector search can often find chunks about each condition independently, '
                       'but it does not guarantee that the same entity satisfies all conditions.\n'
                       '\n'
                       'Graph queries are naturally suited to intersections because the query can '
                       'require multiple graph patterns to hold at once. This is especially useful '
                       'in domains such as compliance, pharmacology, supply chains, and '
                       'organizational hierarchies where the answer is defined by exact '
                       'combinations of relationships.\n'
                       '\n'
                       'The key diagnostic question is: does the answer depend on topical '
                       'similarity, or on satisfying a logical conjunction of constraints?\n'
                       '\n'
                       '\n'
                       '## 4. Failure Mode 3: Chained or Multi-Hop Reasoning\n'
                       '\n'
                       'Multi-hop questions require traversing several relationships in sequence. '
                       'Standard retrieval may retrieve one or two relevant facts, but it does not '
                       'guarantee that those facts can be composed into the exact path required.\n'
                       '\n'
                       'A graph encodes the path directly. The answer can be derived by traversing '
                       'from one entity to another through typed edges and filtering intermediate '
                       'nodes by properties such as year.\n'
                       '\n'
                       'This does not make graph reasoning infallible. The graph itself must be '
                       'correct, entities must be linked properly, and the query must express the '
                       'intended traversal. But when those conditions hold, the graph provides a '
                       'much more deterministic reasoning substrate than loose chunk similarity.\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX01}}\n'
                       '\n'
                       '\n'
                       '## 5. Knowledge Graphs: The Core Mental Model\n'
                       '\n'
                       'A knowledge graph is a network of entities connected by typed '
                       'relationships. The graph is machine-readable because each node and edge '
                       'has explicit meaning.\n'
                       '\n'
                       'In a movie domain, nodes might represent people, movies, characters, '
                       'genres, or text chunks. Edges might represent relationships such as '
                       '`DIRECTED`, `ACTED_IN`, `HAS_GENRE`, `APPEARS_IN`, or `MENTIONS`.\n'
                       '\n'
                       'The graph becomes valuable because a question can be translated into a '
                       'path. Instead of retrieving text that discusses a director, the system can '
                       'traverse a `DIRECTED` relationship from a person node to movie nodes and '
                       'then continue to actor nodes. That distinction—path traversal instead of '
                       'similarity search—is the essence of graph retrieval.\n'
                       '\n'
                       '{{image:movie-knowledge-graph}}'
                       '\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX02}}\n'
                       '\n'
                       '\n'
                       '## 6. Nodes, Entities, and Properties\n'
                       '\n'
                       'A node represents a thing in the domain: a person, organization, product, '
                       'movie, drug, location, event, document, or concept. Nodes usually carry '
                       'properties that describe them.\n'
                       '\n'
                       'Good graph design separates identity from attributes. For example, a movie '
                       'node might be identified by a stable ID while storing title and release '
                       'year as properties. Stable identity is especially important because titles '
                       'and names can change or collide.\n'
                       '\n'
                       'When graph-enhanced RAG fails, entity identity is often one of the first '
                       'areas to inspect. Duplicate nodes, missing identifiers, or overloaded '
                       'properties create downstream retrieval errors that are difficult for the '
                       'LLM to repair.\n'
                       '\n'
                       '\n'
                       '## 7. Edges and Typed Relationships\n'
                       '\n'
                       'Edges encode how entities relate. An edge is not merely a connection; it '
                       'has a type that gives the connection meaning. `ACTED_IN` is different from '
                       '`DIRECTED`, just as `WORKS_AT` is different from `OWNS`.\n'
                       '\n'
                       'Direction matters too. A `Person -[:DIRECTED]-> Movie` relation is '
                       'semantically different from the reverse traversal, even though both nodes '
                       'are connected.\n'
                       '\n'
                       'Typed relationships are what make graphs useful for precise questions. '
                       'They allow the query engine to restrict traversal to only the '
                       'relationships that matter, instead of relying on a language model to infer '
                       'the relationship from surrounding prose.\n'
                       '\n'
                       '\n'
                       '## 8. Graph Databases and Why They Exist\n'
                       '\n'
                       'Graph databases are specialized for storing and traversing nodes and '
                       'edges. They differ from relational databases primarily in how '
                       'relationships are represented and queried.\n'
                       '\n'
                       'The source discusses systems such as Neo4j, Amazon Neptune, Kuzu, and '
                       'TigerGraph. The database choice influences deployment, scaling, query '
                       'language, operational burden, and integration options.\n'
                       '\n'
                       'For RAG, the important point is not the brand. It is that graph traversal '
                       'must be efficient enough to sit inside an interactive query path, and the '
                       'database must support the consistency, security, and lifecycle '
                       'requirements of the application.\n'
                       '\n'
                       '\n'
                       '## 9. Cypher: Reading Graph Patterns\n'
                       '\n'
                       'Cypher is a graph query language strongly associated with property-graph '
                       'databases such as Neo4j. Its syntax visually resembles the path being '
                       'queried.\n'
                       '\n'
                       'A basic pattern can be read as:\n'
                       '\n'
                       '```cypher\n'
                       '(p:Person)-[:DIRECTED]->(m:Movie)\n'
                       '```\n'
                       '\n'
                       'This means: find a `Person` node `p` connected by a `DIRECTED` '
                       'relationship to a `Movie` node `m`.\n'
                       '\n'
                       'A complete query adds filtering and projection:\n'
                       '\n'
                       '```cypher\n'
                       'MATCH (p:Person)-[:DIRECTED]->(m:Movie)\n'
                       "WHERE m.title = 'Oppenheimer'\n"
                       'RETURN p.name\n'
                       '```\n'
                       '\n'
                       'The important learner skill is to read the pattern left to right as a '
                       'relationship statement, not as an opaque database command.\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX03}}\n'
                       '\n'
                       '\n'
                       '## 10. SPARQL and RDF Triples\n'
                       '\n'
                       'SPARQL is a standard query language for RDF-style graphs. RDF represents '
                       'knowledge as triples: subject, predicate, object.\n'
                       '\n'
                       'A conceptually similar query can be expressed as:\n'
                       '\n'
                       '```sparql\n'
                       'SELECT ?personName\n'
                       'WHERE {\n'
                       '  ?movie :title "Oppenheimer" .\n'
                       '  ?person :directed ?movie .\n'
                       '  ?person :name ?personName .\n'
                       '}\n'
                       '```\n'
                       '\n'
                       'Cypher and SPARQL use different data models and syntax, but both let you '
                       'express precise relationship patterns. The practical choice usually '
                       'follows the graph technology already in use.\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX04}}\n'
                       '\n'
                       '\n'
                       '## 11. Ontology Versus Schema\n'
                       '\n'
                       'An ontology defines the conceptual rules of a domain: what types of things '
                       'exist, which relationships are meaningful, and what constraints describe '
                       'reality. A schema is the database-level implementation of that model.\n'
                       '\n'
                       'For example, an ontology may state that a person can direct a movie and '
                       'that a movie has a release year. The schema then defines the corresponding '
                       'node labels, relationship types, and property types in the database.\n'
                       '\n'
                       'This distinction matters in RAG because the ontology helps shape the '
                       'reasoning model, while the concrete schema is what the LLM must know to '
                       'generate valid Cypher or SPARQL.\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX05}}\n'
                       '\n'
                       '\n'
                       '## 12. Designing a Movie Knowledge Graph\n'
                       '\n'
                       'The chapter’s working example combines structured movie metadata with '
                       'unstructured movie scripts. The structured data provides entities and '
                       'verified relationships; the scripts provide text chunks and mentions.\n'
                       '\n'
                       'A useful schema includes nodes such as `Movie`, `Person`, `Character`, '
                       '`Genre`, and `Chunk`, with relationships such as `DIRECTED`, `ACTED_IN`, '
                       '`HAS_GENRE`, `PORTRAYED_BY`, `BELONGS_TO`, and `MENTIONS`.\n'
                       '\n'
                       'The design illustrates a broader pattern: combine structured sources that '
                       'are strong at identity and relationships with unstructured sources that '
                       'contain rich language and evidence.\n'
                       '\n'
                       '\n'
                       '## 13. Chunking Unstructured Text Before Graph Construction\n'
                       '\n'
                       'Unstructured source documents still need ordinary RAG preprocessing. In '
                       'the movie example, scripts are cleaned and split into chunks before those '
                       'chunks become nodes in the graph.\n'
                       '\n'
                       'The key lesson is that adding a graph does not eliminate chunking. '
                       'Instead, chunks become first-class graph entities that can be connected to '
                       'higher-level objects.\n'
                       '\n'
                       'A stable chunk ID becomes especially important because the same chunk may '
                       'exist simultaneously in a vector index and in the graph. That identifier '
                       'acts as the join key between semantic retrieval and graph enrichment.\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX06}}\n'
                       '\n'
                       '\n'
                       '## 14. Entity Detection Is Domain-Specific\n'
                       '\n'
                       'Before a graph can encode relationships, the pipeline must identify '
                       'entities. In movie scripts, uppercase names provide a convenient heuristic '
                       'for detecting characters, but even that clean signal produces false '
                       'positives.\n'
                       '\n'
                       'This illustrates a general rule: entity extraction is never “just run '
                       'NER.” Domain formatting, aliases, abbreviations, IDs, and noisy documents '
                       'affect accuracy.\n'
                       '\n'
                       'Production pipelines therefore combine model-based extraction with '
                       'deterministic rules and validation. The more business-critical the graph, '
                       'the less acceptable it is to let a noisy extraction model silently create '
                       'authoritative nodes.\n'
                       '\n'
                       '\n'
                       '## 15. Connecting Chunks to Domain Entities\n'
                       '\n'
                       'Once entities are identified, chunks can be connected to them. For '
                       'example:\n'
                       '\n'
                       '```text\n'
                       '(Chunk)-[:MENTIONS]->(Character)\n'
                       '(Character)-[:APPEARS_IN]->(Movie)\n'
                       '(Person)-[:ACTED_IN]->(Movie)\n'
                       '(Person)-[:DIRECTED]->(Movie)\n'
                       '```\n'
                       '\n'
                       'This lets a chunk act as both evidence and a bridge into structured '
                       'context. A retrieved chunk can tell the system which character is '
                       'mentioned, and the graph can then supply the actor, movie, director, or '
                       'related entities.\n'
                       '\n'
                       'That pattern is the foundation of chunk enrichment.\n'
                       '\n'
                       '\n'
                       '## 16. Two Main Query-Time Patterns\n'
                       '\n'
                       'The chapter presents two major ways to use a knowledge graph in a RAG '
                       'query flow:\n'
                       '\n'
                       '1. **Chunk enrichment** starts with vector retrieval and uses the graph to '
                       'add missing structured context to retrieved chunks.\n'
                       '2. **Hybrid-graph retrieval** runs graph retrieval as an additional '
                       'retrieval channel, often by translating the user question into Cypher or '
                       'SPARQL.\n'
                       '\n'
                       'These solve different problems. Enrichment assumes semantic retrieval '
                       'already found the right evidence but the evidence is context-poor. Hybrid '
                       'graph retrieval assumes the question itself is relationship-heavy and '
                       'requires graph traversal to discover the answer.\n'
                       '\n'
                       '\n'
                       '## 17. Chunk Enrichment\n'
                       '\n'
                       'Chunk enrichment is a metadata-first strategy. Start with vector '
                       'retrieval, then inspect the entities connected to the retrieved chunk and '
                       'fetch structured facts from the graph.\n'
                       '\n'
                       'Suppose a retrieved dialogue chunk contains the character name “Vincent” '
                       'but not the actor or movie. The graph can enrich it with facts such as the '
                       'canonical character identity, performer, and movie.\n'
                       '\n'
                       'The final prompt contains the original chunk plus this structured context '
                       'packet. This keeps vector search in charge of finding semantically '
                       'relevant text while the graph supplies high-confidence facts needed to '
                       'answer precisely.\n'
                       '\n'
                       '{{image:chunk-enrichment}}'
                       '\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX07}}\n'
                       '\n'
                       '\n'
                       '## 18. Why Chunk Enrichment Is Operationally Attractive\n'
                       '\n'
                       'Chunk enrichment can be relatively low-risk because it does not require an '
                       'LLM to synthesize a complex graph query on every request. If the vector '
                       'search already found a chunk ID, the graph step may be a direct indexed '
                       'lookup.\n'
                       '\n'
                       'That means the graph adds context without taking over the entire retrieval '
                       'path. It is a useful first graph-enhancement pattern when the main failure '
                       'is missing metadata, names, dates, IDs, or relationships around otherwise '
                       'relevant text.\n'
                       '\n'
                       'The trade-off is that enrichment cannot discover evidence that vector '
                       'search never retrieved. It improves context around found chunks rather '
                       'than replacing candidate generation.\n'
                       '\n'
                       '\n'
                       '## 19. Hybrid-Graph Retrieval\n'
                       '\n'
                       'Hybrid-graph retrieval treats the graph as a parallel retrieval engine. A '
                       'natural-language question is translated into a formal graph query, the '
                       'graph returns relevant entities or chunks, and those results are combined '
                       'with vector-retrieved evidence.\n'
                       '\n'
                       'This approach is powerful for multi-hop and constrained questions because '
                       'the graph query can encode the relationship structure explicitly.\n'
                       '\n'
                       'However, it introduces a new failure surface: text-to-Cypher or '
                       'text-to-SPARQL generation. The LLM can produce invalid syntax, reference '
                       'nonexistent labels, create expensive traversals, or misinterpret the '
                       'user’s intent.\n'
                       '\n'
                       '{{image:graph-hybrid-retrieval}}'
                       '\n'
                       '\n'
                       '\n'
                       '## 20. Schema-Conditioned Graph Query Generation\n'
                       '\n'
                       'An LLM cannot reliably generate graph queries if it does not know the '
                       'graph schema. The prompt must expose the available node labels, '
                       'relationships, properties, and important constraints.\n'
                       '\n'
                       'This is analogous to text-to-SQL. The model needs a vocabulary and grammar '
                       'for the database before it can write a valid query.\n'
                       '\n'
                       'A production implementation should treat schema descriptions as versioned '
                       'application assets. If the graph evolves but the prompt still describes '
                       'the old schema, query generation can silently degrade.\n'
                       '\n'
                       '\n'
                       '## 21. Making Text-to-Cypher Safer\n'
                       '\n'
                       'Because LLM-generated graph queries are code-like artifacts executed '
                       'against a database, they require guardrails.\n'
                       '\n'
                       'Useful controls include read-only database credentials, query templates, '
                       'allow-lists for labels and relationship types, complexity limits, '
                       'timeouts, row limits, syntax validation, and retry logic for correctable '
                       'failures.\n'
                       '\n'
                       'The principle is the same as with tool-using agents: the model may propose '
                       'an action, but a deterministic execution layer should decide whether that '
                       'action is allowed and safe.\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX09}}\n'
                       '\n'
                       '\n'
                       '## 22. Combining Vector and Graph Evidence\n'
                       '\n'
                       'Graph results and vector results should be treated as complementary '
                       'evidence channels. The graph is strong at explicit structure and precise '
                       'relationships; the vector index is strong at fuzzy semantic relevance and '
                       'unstructured language.\n'
                       '\n'
                       'A combined pipeline can merge retrieved chunks, attach provenance, remove '
                       'duplicates, and optionally rerank the full candidate set before '
                       'generation.\n'
                       '\n'
                       'The answer generator should know which facts came from which channel. '
                       'Preserving provenance makes debugging and citation generation much '
                       'easier.\n'
                       '\n'
                       '\n'
                       '## 23. Choosing Enrichment or Hybrid Retrieval\n'
                       '\n'
                       'Choose chunk enrichment when vector search usually finds the right text '
                       'but the text lacks enough structured context to answer fully.\n'
                       '\n'
                       'Choose hybrid graph retrieval when the query itself is fundamentally '
                       'relational: multiple hops, intersections, graph-wide constraints, or '
                       'relationship-based discovery.\n'
                       '\n'
                       'The choice should come from evaluation data, not preference. Inspect real '
                       'failure cases from the standard RAG system and classify whether the issue '
                       'is “missing context around a relevant chunk” or “semantic retrieval cannot '
                       'discover the relationship path at all.”\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX08}}\n'
                       '\n'
                       '\n'
                       '## 24. Where Should Embeddings Live?\n'
                       '\n'
                       'Modern graph databases can store vectors directly on chunk nodes, which '
                       'allows semantic search and graph traversal inside one database. This '
                       'reduces synchronization problems and can provide atomic consistency.\n'
                       '\n'
                       'Alternatively, embeddings can remain in a dedicated vector database while '
                       'the graph stores structured relationships. A retrieved chunk ID is then '
                       'used to look up graph context.\n'
                       '\n'
                       'The split design preserves a specialized retrieval stack—hybrid search, '
                       'reranking, vector tuning—but creates a synchronization obligation. The '
                       'unified design simplifies data consistency but may create resource '
                       'contention between vector search and graph traversal.\n'
                       '\n'
                       '\n'
                       '## 25. Keeping Vector and Graph Stores Synchronized\n'
                       '\n'
                       'When vector and graph stores are separate, chunk identity becomes '
                       'critical. Every insertion, update, and deletion must be reflected in both '
                       'systems.\n'
                       '\n'
                       'A stale vector entry that points to a deleted graph node creates broken '
                       'enrichment. A graph node without a corresponding vector entry may become '
                       'undiscoverable by the semantic channel.\n'
                       '\n'
                       'Production systems therefore need stable IDs, versioning, idempotent '
                       'ingestion, reconciliation jobs, and monitoring for orphaned records.\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX10}}\n'
                       '\n'
                       '\n'
                       '## 26. Building Knowledge Graphs Is the Hard Part\n'
                       '\n'
                       'Querying a clean knowledge graph is often easier than building one. The '
                       'real work is defining a useful model, extracting entities, discovering '
                       'relationships, resolving aliases, deduplicating nodes, validating facts, '
                       'and keeping the graph fresh.\n'
                       '\n'
                       'The movie example is unusually friendly because structured metadata '
                       'already exists and scripts have recognizable formatting. Enterprise '
                       'corpora are much messier.\n'
                       '\n'
                       'This is why the decision to add a knowledge graph is primarily a '
                       'data-engineering decision, not only an LLM decision.\n'
                       '\n'
                       '\n'
                       '## 27. Automating KG Construction from Text\n'
                       '\n'
                       'A common automated construction pipeline has three stages:\n'
                       '\n'
                       '1. Identify entities.\n'
                       '2. Extract relationships among those entities.\n'
                       '3. Link multiple surface forms to canonical entities.\n'
                       '\n'
                       'Modern LLMs can propose entities and relation triples directly from '
                       'unstructured text, which simplifies bootstrapping. But extraction quality '
                       'remains domain-dependent.\n'
                       '\n'
                       'A production pipeline commonly adds deterministic validators, classical '
                       'NLP checks, confidence thresholds, and human review for critical facts.\n'
                       '\n'
                       '\n'
                       '## 28. Entity Identification\n'
                       '\n'
                       'Entity identification asks: which spans in the text correspond to things '
                       'that should become nodes?\n'
                       '\n'
                       'The challenge is not only detecting proper names. The system must classify '
                       'the entity type and decide whether the mention is important enough to '
                       'model.\n'
                       '\n'
                       'A strong ontology helps constrain the task. If the graph models only '
                       'companies, people, products, and contracts, the extractor does not need to '
                       'invent arbitrary node types for every noun phrase.\n'
                       '\n'
                       '\n'
                       '## 29. Relation Extraction\n'
                       '\n'
                       'Relation extraction converts language into typed graph edges. From a '
                       'sentence such as “Company A acquired Company B,” the system might propose '
                       'an `ACQUIRED` relationship between two company nodes.\n'
                       '\n'
                       'The edge type must come from a controlled relationship vocabulary if the '
                       'graph is expected to remain queryable and consistent.\n'
                       '\n'
                       'Unconstrained relation labels create schema drift: one extractor may '
                       'produce `FOUNDED_BY`, another `HAS_FOUNDER`, and a third `CREATED_BY`. '
                       'Normalization is therefore part of graph quality.\n'
                       '\n'
                       '\n'
                       '## 30. Entity Linking: One Thing, Many Names\n'
                       '\n'
                       'Entity linking resolves different mentions that refer to the same '
                       'real-world entity. This is one of the hardest steps in production KG '
                       'construction.\n'
                       '\n'
                       'A company can appear under a legal name, an abbreviation, a brand, or a '
                       'legacy name. A drug can appear under brand, generic, and chemical names. A '
                       'product can appear under vendor-specific SKUs.\n'
                       '\n'
                       'If those aliases become separate nodes, the graph fragments reality and '
                       'multi-hop queries become unreliable. Entity resolution must therefore be '
                       'treated as a first-class pipeline, not a cleanup task.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Entity linking and canonicalization | Show several aliases '
                       'such as IBM, I.B.M., and International Business Machines converging into '
                       'one canonical node | Learner should notice that deduplication preserves '
                       'one real-world identity]]\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX11}}\n'
                       '\n'
                       '\n'
                       '## 31. Using an Ontology to Guide Entity Linking\n'
                       '\n'
                       'An ontology gives entity linking a target structure. It defines which '
                       'canonical entity types exist and what identifiers or aliases are '
                       'expected.\n'
                       '\n'
                       'For example, a company entity might have one canonical name and a '
                       'collection of aliases. New mentions can then be matched against the '
                       'existing canonical record rather than automatically creating a new node.\n'
                       '\n'
                       'This reduces entity explosion and creates a more stable basis for graph '
                       'traversal.\n'
                       '\n'
                       '\n'
                       '## 32. Normalization and Candidate Generation\n'
                       '\n'
                       'Entity resolution often begins with normalization: case-folding, '
                       'standardizing abbreviations, cleaning punctuation, and normalizing known '
                       'formats.\n'
                       '\n'
                       'The pipeline then generates plausible candidate matches rather than '
                       'comparing every entity with every other entity. Candidate generation can '
                       'use string similarity, domain identifiers, embeddings, or domain-specific '
                       'rules.\n'
                       '\n'
                       'The final linking decision can combine several signals and defer '
                       'low-confidence cases to human review.\n'
                       '\n'
                       '\n'
                       '## 33. Human-in-the-Loop Entity Resolution\n'
                       '\n'
                       'Human review is most valuable when applied selectively. High-confidence '
                       'matches can be accepted automatically; ambiguous matches can be queued for '
                       'expert review.\n'
                       '\n'
                       'This turns human effort into a quality-control mechanism rather than the '
                       'primary construction method.\n'
                       '\n'
                       'The reviewed decisions can also become training or calibration data for '
                       'future entity-linking models.\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX12}}\n'
                       '\n'
                       '\n'
                       '## 34. Leveraging Standard Ontologies\n'
                       '\n'
                       'Standard ontologies provide a predesigned conceptual model for a domain. '
                       'They reduce the risk of inventing an inconsistent or overly broad graph '
                       'schema.\n'
                       '\n'
                       'The source cites examples such as FIBO in finance. The general lesson is '
                       'to reuse established domain vocabularies when they match the business '
                       'problem.\n'
                       '\n'
                       'A standard ontology does not populate the graph for you, but it provides a '
                       'disciplined blueprint for entity types and relationships.\n'
                       '\n'
                       '\n'
                       '## 35. Leveraging Curated or Licensed Knowledge Graphs\n'
                       '\n'
                       'Sometimes the hardest part of graph construction—identity resolution—has '
                       'already been done by a specialist provider. Curated datasets can provide '
                       'canonical identifiers and pre-resolved relationships.\n'
                       '\n'
                       'This can dramatically reduce internal entity-linking effort, but '
                       'introduces licensing cost, dependency, and data-model lock-in.\n'
                       '\n'
                       'The decision resembles using a managed RAG platform: buy operational '
                       'leverage in exchange for less control and a long-term provider '
                       'dependency.\n'
                       '\n'
                       '\n'
                       '## 36. Microsoft GraphRAG: A Different Use of Graphs\n'
                       '\n'
                       'The term GraphRAG is sometimes used loosely for any graph-enhanced RAG. '
                       'The chapter uses it more specifically for Microsoft Research’s approach to '
                       'answering broad sensemaking questions.\n'
                       '\n'
                       'GraphRAG is designed for questions that require a global view of a corpus '
                       'rather than retrieving a few local chunks. It builds a graph from source '
                       'documents, detects communities, summarizes those communities, and then '
                       'answers queries using the hierarchy of summaries.\n'
                       '\n'
                       'This is better understood as query-focused summarization over '
                       'graph-derived communities than as ordinary graph traversal.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Microsoft GraphRAG overview | Show source documents '
                       'becoming an entity graph, graph communities, hierarchical community '
                       'summaries, and query-focused summarization | Learner should notice the '
                       'difference between local chunks and global summaries]]\n'
                       '\n'
                       '\n'
                       '## 37. GraphRAG Indexing Pipeline\n'
                       '\n'
                       'GraphRAG indexing is computationally expensive because it performs several '
                       'reasoning-heavy steps before any user query arrives.\n'
                       '\n'
                       'The pipeline extracts entities and relationships, resolves or organizes '
                       'them into a graph, runs community-detection algorithms, and generates '
                       'summaries at multiple levels.\n'
                       '\n'
                       'The advantage is that expensive understanding work is moved into indexing, '
                       'enabling broad queries later. The disadvantage is that corpus updates can '
                       'trigger costly reprocessing.\n'
                       '\n'
                       '\n'
                       '## 38. Community Detection and Hierarchical Summaries\n'
                       '\n'
                       'Community detection groups densely connected parts of the graph into '
                       'coherent clusters. Each cluster can represent a topic, theme, or local '
                       'subnetwork in the corpus.\n'
                       '\n'
                       'An LLM then produces summaries for these communities. Higher-level '
                       'communities summarize larger parts of the graph, creating a hierarchy from '
                       'detailed local structure to broad themes.\n'
                       '\n'
                       'The hierarchy is what makes global sensemaking possible: the system can '
                       'reason over summaries of the whole corpus rather than hoping a small top-k '
                       'retrieval set represents the global picture.\n'
                       '\n'
                       '\n'
                       '## 39. GraphRAG Local Search Versus Global Search\n'
                       '\n'
                       'GraphRAG distinguishes between local and global query strategies.\n'
                       '\n'
                       '**Local search** starts from seed entities and expands around their graph '
                       'neighborhood. It is suited to detailed questions where the answer is '
                       'likely near specific entities.\n'
                       '\n'
                       '**Global search** works over broader community summaries and is suited to '
                       'high-level synthesis across the corpus.\n'
                       '\n'
                       'The distinction mirrors a general retrieval principle: choose a search '
                       'strategy that matches the scope of the question.\n'
                       '\n'
                       '[[IMAGE_NEEDED: GraphRAG local versus global search | Contrast seed-node '
                       'neighborhood expansion with top-down search over community summaries | '
                       'Learner should notice that query scope determines the search strategy]]\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX13}}\n'
                       '\n'
                       '\n'
                       '## 40. The Cost of GraphRAG\n'
                       '\n'
                       'GraphRAG can require many LLM calls during indexing. The chapter’s small '
                       'demonstration already incurs meaningful cost and runtime, illustrating how '
                       'rapidly this can grow for enterprise-scale corpora.\n'
                       '\n'
                       'The important lesson is not the exact dollar value of one example. It is '
                       'that GraphRAG converts indexing from a mostly embedding-oriented pipeline '
                       'into a multi-stage LLM processing job.\n'
                       '\n'
                       'That makes cost estimation, batching, refresh strategy, and evaluation '
                       'essential before adopting it widely.\n'
                       '\n'
                       '\n'
                       '## 41. When GraphRAG Is the Wrong Tool\n'
                       '\n'
                       'GraphRAG is a poor fit when the corpus changes rapidly, when interactive '
                       'latency is critical, when queries require exact verbatim evidence, or when '
                       'most questions are simple factual lookups.\n'
                       '\n'
                       'Its community summaries are intentionally abstract. That is useful for '
                       'broad themes but can be too lossy for legal, audit, or citation-heavy '
                       'workflows.\n'
                       '\n'
                       'A system can therefore use GraphRAG selectively for sensemaking while '
                       'keeping ordinary RAG for exact evidence retrieval.\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX14}}\n'
                       '\n'
                       '\n'
                       '## 42. Graph Database Infrastructure Is a Long-Term Commitment\n'
                       '\n'
                       'Adding a graph database introduces a new stateful system that must be '
                       'deployed, secured, monitored, backed up, upgraded, and kept synchronized '
                       'with changing source data.\n'
                       '\n'
                       'The operational cost persists long after the first successful demo. Graph '
                       'performance depends heavily on memory, index design, traversal patterns, '
                       'and graph shape.\n'
                       '\n'
                       'Before adding a graph, the team should ask whether it has the '
                       'data-engineering and database expertise to operate it over time.\n'
                       '\n'
                       '\n'
                       '## 43. Graph Deployment Models\n'
                       '\n'
                       'The chapter outlines three broad infrastructure models.\n'
                       '\n'
                       'A **traditional server or cluster** gives maximum control but requires the '
                       'team to manage stateful infrastructure.\n'
                       '\n'
                       'A **managed cloud graph service** outsources much of the operational '
                       'burden but adds cloud cost and provider dependence.\n'
                       '\n'
                       'An **embedded graph library** runs inside the application and can be '
                       'attractive for smaller, mostly read-only graphs, but shifts the challenge '
                       'toward build and deployment lifecycle management.\n'
                       '\n'
                       'The best model depends on graph size, update frequency, security '
                       'constraints, and operations maturity.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Graph database deployment choices | Compare self-managed '
                       'cluster, managed cloud graph service, and embedded graph library | Learner '
                       'should notice the trade-off between control and operational burden]]\n'
                       '\n'
                       '\n'
                       '## 44. Knowledge-Graph ETL and Idempotency\n'
                       '\n'
                       'Graph ingestion is vulnerable to partial failures because it often '
                       'involves many dependent node and edge operations.\n'
                       '\n'
                       'A restartable pipeline should be idempotent: rerunning the same operation '
                       'should converge on the same graph instead of duplicating entities or '
                       'relationships.\n'
                       '\n'
                       'In Cypher, `MERGE` is a common tool for this because it checks for a '
                       'matching pattern before creating it. Combined with batching, idempotency '
                       'lets large graph builds recover from failure without one enormous '
                       'transaction.\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX15}}\n'
                       '\n'
                       '\n'
                       '## 45. Schema Evolution\n'
                       '\n'
                       'Although graph databases are often described as flexible or schema-light, '
                       'RAG applications still depend on a predictable graph structure.\n'
                       '\n'
                       'If labels, properties, or relationships change, the LLM’s graph-query '
                       'generation logic must evolve with them. Migrations may need to update '
                       'millions of existing nodes and edges.\n'
                       '\n'
                       'Schema versioning therefore belongs in the same change-management '
                       'discipline as code and prompts.\n'
                       '\n'
                       '\n'
                       '## 46. Graph Performance and Supernodes\n'
                       '\n'
                       'Traversal cost depends on graph depth and topology. Some nodes connect to '
                       'an enormous number of neighbors—so-called supernodes—and can make '
                       'seemingly simple traversals expensive.\n'
                       '\n'
                       'Performance engineering includes profiling queries, indexing frequently '
                       'filtered properties, limiting traversal depth, restructuring hot paths, '
                       'and provisioning enough memory for the working graph.\n'
                       '\n'
                       'This is specialized database work and should be included in the project’s '
                       'staffing and cost model.\n'
                       '\n'
                       '\n'
                       '## 47. Security, Backup, and High Availability\n'
                       '\n'
                       'A graph database may combine sensitive relationships from many systems, '
                       'making access control especially important.\n'
                       '\n'
                       'Security must include encryption, backups, restore testing, high '
                       'availability, and role-based authorization. In some applications, '
                       'permissions may need to apply at node, relationship, or property level.\n'
                       '\n'
                       'A graph that enables the LLM to traverse relationships across departments '
                       'can create data leakage if permissions are not enforced before information '
                       'reaches generation.\n'
                       '\n'
                       '\n'
                       '## 48. Maintaining a Living Graph\n'
                       '\n'
                       'A useful production graph must evolve with the real world. Full rebuilds '
                       'become impractical as the graph grows and source systems change '
                       'continuously.\n'
                       '\n'
                       'The system therefore needs incremental update mechanisms that add, modify, '
                       'retire, and merge facts without corrupting existing structure.\n'
                       '\n'
                       'The challenge is not merely freshness. Historical facts may need to be '
                       'preserved while their current status changes.\n'
                       '\n'
                       '\n'
                       '## 49. CDC Versus Event-Driven Graph Updates\n'
                       '\n'
                       'Structured database sources can use change data capture (CDC) to observe '
                       'inserts, updates, and deletes and translate them into graph operations.\n'
                       '\n'
                       'Unstructured sources often fit an event-driven pattern. A new document '
                       'arriving in object storage can trigger extraction only for that document, '
                       'producing incremental nodes and edges.\n'
                       '\n'
                       'Both patterns avoid rebuilding the entire graph and make freshness more '
                       'manageable.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Living graph update pipeline | Show CDC from databases and '
                       'event-driven processing from document storage both feeding incremental '
                       'graph MERGE/DELETE operations | Learner should notice that freshness is '
                       'maintained incrementally rather than by full rebuilds]]\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX16}}\n'
                       '\n'
                       '\n'
                       '## 50. Handling Entity Merges\n'
                       '\n'
                       'A long-running graph will eventually discover that two nodes represent the '
                       'same real-world entity. The system must merge them without losing valid '
                       'relationships.\n'
                       '\n'
                       'A merge usually selects one canonical survivor node, remaps the other '
                       'node’s relationships, reconciles properties, and removes or redirects the '
                       'duplicate.\n'
                       '\n'
                       'Because merges alter graph topology, they should be observable and '
                       'auditable.\n'
                       '\n'
                       '\n'
                       '## 51. Fact Lifecycle and Tombstoning\n'
                       '\n'
                       'Some facts should not be deleted when they stop being current. A past '
                       'employment relationship, for example, may remain historically useful even '
                       'after it becomes inactive.\n'
                       '\n'
                       'One pattern is to mark the relationship with status or validity metadata '
                       'rather than deleting it. Queries that ask about the present can then '
                       'filter for active relationships, while historical queries retain access to '
                       'the past.\n'
                       '\n'
                       'This is essential for time-bound questions and auditability.\n'
                       '\n'
                       '\n'
                       '## 52. The Accuracy–Cost Trade-Off\n'
                       '\n'
                       'Knowledge-enhanced RAG is an architectural investment. The expected '
                       'benefit is higher accuracy on queries that depend on relationships, '
                       'constraints, or global structure. The cost is additional data modeling, '
                       'ETL, infrastructure, evaluation, security, and long-term maintenance.\n'
                       '\n'
                       'The correct baseline is therefore not “graphs are more advanced.” The '
                       'baseline is “does standard or hybrid RAG already meet the requirement?”\n'
                       '\n'
                       'Only measured failure modes should justify the additional graph layer.\n'
                       '\n'
                       '\n'
                       '## 53. A Practical KG ROI Checklist\n'
                       '\n'
                       'The chapter proposes evaluating several conditions before making a major '
                       'KG investment:\n'
                       '\n'
                       '- Does standard RAG repeatedly fail on multi-hop, time-bound, or tightly '
                       'constrained questions?\n'
                       '- Does the domain require deterministic grounding around important '
                       'entities?\n'
                       '- Is there an existing ontology or curated graph that reduces construction '
                       'effort?\n'
                       '- Does the domain naturally derive value from relationships?\n'
                       '- Can the organization own graph modeling and ETL long-term?\n'
                       '- Are the expected accuracy gains tied to concrete business value?\n'
                       '\n'
                       'The checklist is a forcing function for disciplined architecture '
                       'decisions.\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX17}}\n'
                       '\n'
                       '\n'
                       '## 54. Comparing RAG Architectures\n'
                       '\n'
                       'Different RAG architectures solve different classes of problems.\n'
                       '\n'
                       'Standard vector RAG is strong for semantic retrieval over unstructured '
                       'text. Keyword hybrid search adds exact-term matching. KG-hybrid RAG adds '
                       'precise relationships and constraints. Microsoft GraphRAG adds broad '
                       'sensemaking across a corpus. Agentic RAG adds iterative planning and tool '
                       'use.\n'
                       '\n'
                       'These approaches can coexist. A mature system may route a query to the '
                       'simplest architecture that can answer it reliably rather than forcing '
                       'every query through the most expensive path.\n'
                       '\n'
                       '\n'
                       '## 55. Use Evaluation to Decide When to Add a Graph\n'
                       '\n'
                       'Chapter 6’s evaluation discipline is especially important here. Before '
                       'building a knowledge graph, collect the queries that standard RAG fails.\n'
                       '\n'
                       'Cluster those failures by cause. If many are relationship-heavy, '
                       'time-bound, or multi-hop, a graph pilot becomes evidence-driven rather '
                       'than speculative.\n'
                       '\n'
                       'After implementing the graph enhancement, evaluate the same failure set '
                       'again and compare quality, latency, and cost. The graph should earn its '
                       'operational complexity through measurable improvement.\n'
                       '\n'
                       '\n'
                       '## 56. Production Blueprint for Knowledge-Enhanced RAG\n'
                       '\n'
                       'A practical production architecture can keep the ordinary RAG pipeline '
                       'intact while adding a graph service as an optional evidence channel.\n'
                       '\n'
                       'The query router classifies whether graph support is needed. Standard '
                       'semantic or hybrid retrieval produces text candidates. If enrichment is '
                       'required, chunk IDs trigger graph lookups. If structural discovery is '
                       'required, a guarded text-to-Cypher component runs a graph query. Results '
                       'are normalized, deduplicated, reranked if appropriate, and sent to '
                       'generation with provenance.\n'
                       '\n'
                       'On the ingestion side, stable IDs, versioned schemas, entity resolution, '
                       'incremental updates, and reconciliation jobs keep vector and graph stores '
                       'consistent.\n'
                       '\n'
                       '[[IMAGE_NEEDED: Knowledge-Enhanced RAG production architecture | Show '
                       'ingestion into vector and graph stores, query routing, vector retrieval, '
                       'graph enrichment/hybrid graph retrieval, evidence merge, reranking, and '
                       'LLM generation | Learner should notice that the graph is an additional '
                       'evidence channel, not a replacement for the RAG stack]]\n'
                       '\n'
                       '\n'
                       '## 57. Diagnosing Knowledge-Enhanced RAG Failures\n'
                       '\n'
                       'When an answer is wrong, isolate the failing layer.\n'
                       '\n'
                       'If the correct relation is absent from the graph, the construction '
                       'pipeline failed. If duplicate entities split the relationship path, entity '
                       'linking failed. If the graph contains the answer but the generated Cypher '
                       'does not retrieve it, query generation failed. If the graph and query are '
                       'correct but the final answer is wrong, the generation layer failed.\n'
                       '\n'
                       'This layered diagnosis prevents the team from “fixing the prompt” when the '
                       'actual problem is data quality or graph maintenance.\n'
                       '\n'
                       '\n'
                       '{{exercise:M01.L09.EX18}}\n'
                       '\n'
                       '## 58. Common Misconceptions\n'
                       '\n'
                       '**“A knowledge graph is automatically more accurate than vector '
                       'search.”**  \n'
                       'A graph can only be as reliable as its entities, relationships, and update '
                       'pipeline. A wrong or fragmented graph can produce deterministic but '
                       'incorrect answers.\n'
                       '\n'
                       '**“GraphRAG means any RAG system that touches a graph.”**  \n'
                       'The source uses *GraphRAG* specifically for Microsoft Research’s '
                       'community-based, query-focused summarization approach. Ordinary '
                       'KG-enhanced RAG includes other patterns such as chunk enrichment and '
                       'hybrid graph retrieval.\n'
                       '\n'
                       '**“If an LLM can generate Cypher, graph retrieval is solved.”**  \n'
                       'Text-to-Cypher adds a new failure surface. The LLM needs the current '
                       'schema, and the execution layer still needs validation, least privilege, '
                       'timeouts, and limits.\n'
                       '\n'
                       '**“Entity extraction is the hard part; entity linking is easy.”**  \n'
                       'In enterprise data, determining that multiple names refer to the same '
                       'real-world entity is often one of the hardest and most persistent '
                       'problems.\n'
                       '\n'
                       '**“A graph removes the need for chunking and vector retrieval.”**  \n'
                       'Knowledge-enhanced RAG often keeps ordinary chunking, embeddings, hybrid '
                       'search, and reranking. The graph adds structure; it does not erase the '
                       'text pipeline.\n'
                       '\n'
                       '**“GraphRAG is ideal for every broad enterprise corpus.”**  \n'
                       'GraphRAG can be costly to index and maintain, and its summaries can be too '
                       'lossy for verbatim-citation or rapidly changing workloads.\n'
                       '\n'
                       '**“Deleting expired facts is always correct.”**  \n'
                       'Historical questions may require old relationships. Status fields or '
                       'temporal validity are often safer than destructive deletion.\n'
                       '\n'
                       '**“Schema-less means schema management does not matter.”**  \n'
                       'The application and text-to-query prompt still depend on stable labels, '
                       'relationships, and properties. Schema changes need versioning and '
                       'migration discipline.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 59. Terminology Reference\n'
                       '\n'
                       '| Term | Meaning in this lesson |\n'
                       '|---|---|\n'
                       '| Knowledge graph (KG) | A machine-readable network of entities connected '
                       'by typed relationships |\n'
                       '| Node / entity | A real-world thing represented in the graph |\n'
                       '| Edge / relationship | A typed connection between nodes |\n'
                       '| Property | An attribute stored on a node or relationship |\n'
                       '| Cypher | A property-graph query language commonly associated with Neo4j '
                       '|\n'
                       '| SPARQL | A standard query language for RDF graphs and triple stores |\n'
                       '| Ontology | The conceptual model and rules that define a domain |\n'
                       '| Schema | The database-level implementation of labels, relationships, and '
                       'properties |\n'
                       '| Chunk enrichment | Adding graph-derived structured context to a chunk '
                       'retrieved by ordinary RAG |\n'
                       '| Hybrid graph retrieval | Combining graph-query results with vector or '
                       'hybrid text retrieval |\n'
                       '| Text-to-Cypher | Translating natural-language questions into Cypher '
                       'queries |\n'
                       '| Entity identification | Detecting entity mentions and their types in '
                       'source data |\n'
                       '| Relation extraction | Converting statements into typed relationships |\n'
                       '| Entity linking | Mapping multiple mentions or aliases to one canonical '
                       'entity |\n'
                       '| Canonical entity | The authoritative graph node representing a '
                       'real-world thing |\n'
                       '| Community detection | Grouping densely connected graph regions |\n'
                       '| GraphRAG | In this lesson, Microsoft Research’s graph/community-based '
                       'query-focused summarization approach |\n'
                       '| Local search | GraphRAG search centered on local graph neighborhoods |\n'
                       '| Global search | GraphRAG search over broad community summaries |\n'
                       '| Idempotency | Property that lets an ingestion task be retried without '
                       'creating duplicate side effects |\n'
                       '| CDC | Change data capture, which turns source-database changes into '
                       'downstream update events |\n'
                       '| Tombstoning | Marking a fact inactive or expired without deleting its '
                       'historical existence |\n'
                       '| Supernode | A graph node with exceptionally many connections that may '
                       'create traversal hotspots |\n'
                       '| Provenance | Metadata showing where evidence came from and how it was '
                       'transformed |\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## 60. Retain This Mental Model\n'
                       '\n'
                       '**Vector search asks:** *What text is semantically similar?*  \n'
                       '**Keyword search asks:** *What text contains the exact terms?*  \n'
                       '**A knowledge graph asks:** *What entities are connected by the required '
                       'relationships?*  \n'
                       '**GraphRAG asks:** *What global structure and themes emerge across the '
                       'corpus?*  \n'
                       '**Agentic RAG asks:** *What sequence of retrieval and tool-use steps '
                       'should I perform to solve this task?*\n'
                       '\n'
                       'A production system should route each query toward the simplest mechanism '
                       'that can answer it reliably.\n'
                       '\n'
                       'The graph earns its place only when the accuracy gained from explicit '
                       'structure is worth the engineering required to build, link, update, '
                       'secure, and operate that structure.\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Comprehensive self-check\n'
                       '\n'
                       '1. What problem or design decision does **Why Knowledge-Enhanced RAG '
                       'Exists** address in knowledge-enhanced RAG?\n'
                       '2. What is one failure mode or trade-off you would monitor when applying '
                       '**Why Knowledge-Enhanced RAG Exists** in production?\n'
                       '3. What problem or design decision does **Failure Mode 1: Time-Bound '
                       'Facts** address in knowledge-enhanced RAG?\n'
                       '4. What is one failure mode or trade-off you would monitor when applying '
                       '**Failure Mode 1: Time-Bound Facts** in production?\n'
                       '5. What problem or design decision does **Failure Mode 2: Intersections of '
                       'Constraints** address in knowledge-enhanced RAG?\n'
                       '6. What is one failure mode or trade-off you would monitor when applying '
                       '**Failure Mode 2: Intersections of Constraints** in production?\n'
                       '7. What problem or design decision does **Failure Mode 3: Chained or '
                       'Multi-Hop Reasoning** address in knowledge-enhanced RAG?\n'
                       '8. What is one failure mode or trade-off you would monitor when applying '
                       '**Failure Mode 3: Chained or Multi-Hop Reasoning** in production?\n'
                       '9. What problem or design decision does **Knowledge Graphs: The Core '
                       'Mental Model** address in knowledge-enhanced RAG?\n'
                       '10. What is one failure mode or trade-off you would monitor when applying '
                       '**Knowledge Graphs: The Core Mental Model** in production?\n'
                       '11. What problem or design decision does **Nodes, Entities, and '
                       'Properties** address in knowledge-enhanced RAG?\n'
                       '12. What is one failure mode or trade-off you would monitor when applying '
                       '**Nodes, Entities, and Properties** in production?\n'
                       '13. What problem or design decision does **Edges and Typed Relationships** '
                       'address in knowledge-enhanced RAG?\n'
                       '14. What is one failure mode or trade-off you would monitor when applying '
                       '**Edges and Typed Relationships** in production?\n'
                       '15. What problem or design decision does **Graph Databases and Why They '
                       'Exist** address in knowledge-enhanced RAG?\n'
                       '16. What is one failure mode or trade-off you would monitor when applying '
                       '**Graph Databases and Why They Exist** in production?\n'
                       '17. What problem or design decision does **Cypher: Reading Graph '
                       'Patterns** address in knowledge-enhanced RAG?\n'
                       '18. What is one failure mode or trade-off you would monitor when applying '
                       '**Cypher: Reading Graph Patterns** in production?\n'
                       '19. What problem or design decision does **SPARQL and RDF Triples** '
                       'address in knowledge-enhanced RAG?\n'
                       '20. What is one failure mode or trade-off you would monitor when applying '
                       '**SPARQL and RDF Triples** in production?\n'
                       '21. What problem or design decision does **Ontology Versus Schema** '
                       'address in knowledge-enhanced RAG?\n'
                       '22. What is one failure mode or trade-off you would monitor when applying '
                       '**Ontology Versus Schema** in production?\n'
                       '23. What problem or design decision does **Designing a Movie Knowledge '
                       'Graph** address in knowledge-enhanced RAG?\n'
                       '24. What is one failure mode or trade-off you would monitor when applying '
                       '**Designing a Movie Knowledge Graph** in production?\n'
                       '25. What problem or design decision does **Chunking Unstructured Text '
                       'Before Graph Construction** address in knowledge-enhanced RAG?\n'
                       '26. What is one failure mode or trade-off you would monitor when applying '
                       '**Chunking Unstructured Text Before Graph Construction** in production?\n'
                       '27. What problem or design decision does **Entity Detection Is '
                       'Domain-Specific** address in knowledge-enhanced RAG?\n'
                       '28. What is one failure mode or trade-off you would monitor when applying '
                       '**Entity Detection Is Domain-Specific** in production?\n'
                       '29. What problem or design decision does **Connecting Chunks to Domain '
                       'Entities** address in knowledge-enhanced RAG?\n'
                       '30. What is one failure mode or trade-off you would monitor when applying '
                       '**Connecting Chunks to Domain Entities** in production?\n'
                       '31. What problem or design decision does **Two Main Query-Time Patterns** '
                       'address in knowledge-enhanced RAG?\n'
                       '32. What is one failure mode or trade-off you would monitor when applying '
                       '**Two Main Query-Time Patterns** in production?\n'
                       '33. What problem or design decision does **Chunk Enrichment** address in '
                       'knowledge-enhanced RAG?\n'
                       '34. What is one failure mode or trade-off you would monitor when applying '
                       '**Chunk Enrichment** in production?\n'
                       '35. What problem or design decision does **Why Chunk Enrichment Is '
                       'Operationally Attractive** address in knowledge-enhanced RAG?\n'
                       '36. What is one failure mode or trade-off you would monitor when applying '
                       '**Why Chunk Enrichment Is Operationally Attractive** in production?\n'
                       '37. What problem or design decision does **Hybrid-Graph Retrieval** '
                       'address in knowledge-enhanced RAG?\n'
                       '38. What is one failure mode or trade-off you would monitor when applying '
                       '**Hybrid-Graph Retrieval** in production?\n'
                       '39. What problem or design decision does **Schema-Conditioned Graph Query '
                       'Generation** address in knowledge-enhanced RAG?\n'
                       '40. What is one failure mode or trade-off you would monitor when applying '
                       '**Schema-Conditioned Graph Query Generation** in production?\n'
                       '41. What problem or design decision does **Making Text-to-Cypher Safer** '
                       'address in knowledge-enhanced RAG?\n'
                       '42. What is one failure mode or trade-off you would monitor when applying '
                       '**Making Text-to-Cypher Safer** in production?\n'
                       '43. What problem or design decision does **Combining Vector and Graph '
                       'Evidence** address in knowledge-enhanced RAG?\n'
                       '44. What is one failure mode or trade-off you would monitor when applying '
                       '**Combining Vector and Graph Evidence** in production?\n'
                       '45. What problem or design decision does **Choosing Enrichment or Hybrid '
                       'Retrieval** address in knowledge-enhanced RAG?\n'
                       '46. What is one failure mode or trade-off you would monitor when applying '
                       '**Choosing Enrichment or Hybrid Retrieval** in production?\n'
                       '47. What problem or design decision does **Where Should Embeddings Live?** '
                       'address in knowledge-enhanced RAG?\n'
                       '48. What is one failure mode or trade-off you would monitor when applying '
                       '**Where Should Embeddings Live?** in production?\n'
                       '49. What problem or design decision does **Keeping Vector and Graph Stores '
                       'Synchronized** address in knowledge-enhanced RAG?\n'
                       '50. What is one failure mode or trade-off you would monitor when applying '
                       '**Keeping Vector and Graph Stores Synchronized** in production?\n'
                       '51. What problem or design decision does **Building Knowledge Graphs Is '
                       'the Hard Part** address in knowledge-enhanced RAG?\n'
                       '52. What is one failure mode or trade-off you would monitor when applying '
                       '**Building Knowledge Graphs Is the Hard Part** in production?\n'
                       '53. What problem or design decision does **Automating KG Construction from '
                       'Text** address in knowledge-enhanced RAG?\n'
                       '54. What is one failure mode or trade-off you would monitor when applying '
                       '**Automating KG Construction from Text** in production?\n'
                       '55. What problem or design decision does **Entity Identification** address '
                       'in knowledge-enhanced RAG?\n'
                       '56. What is one failure mode or trade-off you would monitor when applying '
                       '**Entity Identification** in production?\n'
                       '57. What problem or design decision does **Relation Extraction** address '
                       'in knowledge-enhanced RAG?\n'
                       '58. What is one failure mode or trade-off you would monitor when applying '
                       '**Relation Extraction** in production?\n'
                       '59. What problem or design decision does **Entity Linking: One Thing, Many '
                       'Names** address in knowledge-enhanced RAG?\n'
                       '60. What is one failure mode or trade-off you would monitor when applying '
                       '**Entity Linking: One Thing, Many Names** in production?\n'
                       '61. What problem or design decision does **Using an Ontology to Guide '
                       'Entity Linking** address in knowledge-enhanced RAG?\n'
                       '62. What is one failure mode or trade-off you would monitor when applying '
                       '**Using an Ontology to Guide Entity Linking** in production?\n'
                       '63. What problem or design decision does **Normalization and Candidate '
                       'Generation** address in knowledge-enhanced RAG?\n'
                       '64. What is one failure mode or trade-off you would monitor when applying '
                       '**Normalization and Candidate Generation** in production?\n'
                       '65. What problem or design decision does **Human-in-the-Loop Entity '
                       'Resolution** address in knowledge-enhanced RAG?\n'
                       '66. What is one failure mode or trade-off you would monitor when applying '
                       '**Human-in-the-Loop Entity Resolution** in production?\n'
                       '67. What problem or design decision does **Leveraging Standard '
                       'Ontologies** address in knowledge-enhanced RAG?\n'
                       '68. What is one failure mode or trade-off you would monitor when applying '
                       '**Leveraging Standard Ontologies** in production?\n'
                       '69. What problem or design decision does **Leveraging Curated or Licensed '
                       'Knowledge Graphs** address in knowledge-enhanced RAG?\n'
                       '70. What is one failure mode or trade-off you would monitor when applying '
                       '**Leveraging Curated or Licensed Knowledge Graphs** in production?\n'
                       '71. What problem or design decision does **Microsoft GraphRAG: A Different '
                       'Use of Graphs** address in knowledge-enhanced RAG?\n'
                       '72. What is one failure mode or trade-off you would monitor when applying '
                       '**Microsoft GraphRAG: A Different Use of Graphs** in production?\n'
                       '73. What problem or design decision does **GraphRAG Indexing Pipeline** '
                       'address in knowledge-enhanced RAG?\n'
                       '74. What is one failure mode or trade-off you would monitor when applying '
                       '**GraphRAG Indexing Pipeline** in production?\n'
                       '75. What problem or design decision does **Community Detection and '
                       'Hierarchical Summaries** address in knowledge-enhanced RAG?\n'
                       '76. What is one failure mode or trade-off you would monitor when applying '
                       '**Community Detection and Hierarchical Summaries** in production?\n'
                       '77. What problem or design decision does **GraphRAG Local Search Versus '
                       'Global Search** address in knowledge-enhanced RAG?\n'
                       '78. What is one failure mode or trade-off you would monitor when applying '
                       '**GraphRAG Local Search Versus Global Search** in production?\n'
                       '79. What problem or design decision does **The Cost of GraphRAG** address '
                       'in knowledge-enhanced RAG?\n'
                       '80. What is one failure mode or trade-off you would monitor when applying '
                       '**The Cost of GraphRAG** in production?\n'
                       '81. What problem or design decision does **When GraphRAG Is the Wrong '
                       'Tool** address in knowledge-enhanced RAG?\n'
                       '82. What is one failure mode or trade-off you would monitor when applying '
                       '**When GraphRAG Is the Wrong Tool** in production?\n'
                       '83. What problem or design decision does **Graph Database Infrastructure '
                       'Is a Long-Term Commitment** address in knowledge-enhanced RAG?\n'
                       '84. What is one failure mode or trade-off you would monitor when applying '
                       '**Graph Database Infrastructure Is a Long-Term Commitment** in '
                       'production?\n'
                       '85. What problem or design decision does **Graph Deployment Models** '
                       'address in knowledge-enhanced RAG?\n'
                       '86. What is one failure mode or trade-off you would monitor when applying '
                       '**Graph Deployment Models** in production?\n'
                       '87. What problem or design decision does **Knowledge-Graph ETL and '
                       'Idempotency** address in knowledge-enhanced RAG?\n'
                       '88. What is one failure mode or trade-off you would monitor when applying '
                       '**Knowledge-Graph ETL and Idempotency** in production?\n'
                       '89. What problem or design decision does **Schema Evolution** address in '
                       'knowledge-enhanced RAG?\n'
                       '90. What is one failure mode or trade-off you would monitor when applying '
                       '**Schema Evolution** in production?\n'
                       '91. What problem or design decision does **Graph Performance and '
                       'Supernodes** address in knowledge-enhanced RAG?\n'
                       '92. What is one failure mode or trade-off you would monitor when applying '
                       '**Graph Performance and Supernodes** in production?\n'
                       '93. What problem or design decision does **Security, Backup, and High '
                       'Availability** address in knowledge-enhanced RAG?\n'
                       '94. What is one failure mode or trade-off you would monitor when applying '
                       '**Security, Backup, and High Availability** in production?\n'
                       '95. What problem or design decision does **Maintaining a Living Graph** '
                       'address in knowledge-enhanced RAG?\n'
                       '96. What is one failure mode or trade-off you would monitor when applying '
                       '**Maintaining a Living Graph** in production?\n'
                       '97. What problem or design decision does **CDC Versus Event-Driven Graph '
                       'Updates** address in knowledge-enhanced RAG?\n'
                       '98. What is one failure mode or trade-off you would monitor when applying '
                       '**CDC Versus Event-Driven Graph Updates** in production?\n'
                       '99. What problem or design decision does **Handling Entity Merges** '
                       'address in knowledge-enhanced RAG?\n'
                       '100. What is one failure mode or trade-off you would monitor when applying '
                       '**Handling Entity Merges** in production?\n'
                       '101. What problem or design decision does **Fact Lifecycle and '
                       'Tombstoning** address in knowledge-enhanced RAG?\n'
                       '102. What is one failure mode or trade-off you would monitor when applying '
                       '**Fact Lifecycle and Tombstoning** in production?\n'
                       '103. What problem or design decision does **The Accuracy–Cost Trade-Off** '
                       'address in knowledge-enhanced RAG?\n'
                       '104. What is one failure mode or trade-off you would monitor when applying '
                       '**The Accuracy–Cost Trade-Off** in production?\n'
                       '105. What problem or design decision does **A Practical KG ROI Checklist** '
                       'address in knowledge-enhanced RAG?\n'
                       '106. What is one failure mode or trade-off you would monitor when applying '
                       '**A Practical KG ROI Checklist** in production?\n'
                       '107. What problem or design decision does **Comparing RAG Architectures** '
                       'address in knowledge-enhanced RAG?\n'
                       '108. What is one failure mode or trade-off you would monitor when applying '
                       '**Comparing RAG Architectures** in production?\n'
                       '109. What problem or design decision does **Use Evaluation to Decide When '
                       'to Add a Graph** address in knowledge-enhanced RAG?\n'
                       '110. What is one failure mode or trade-off you would monitor when applying '
                       '**Use Evaluation to Decide When to Add a Graph** in production?\n'
                       '111. What problem or design decision does **Production Blueprint for '
                       'Knowledge-Enhanced RAG** address in knowledge-enhanced RAG?\n'
                       '112. What is one failure mode or trade-off you would monitor when applying '
                       '**Production Blueprint for Knowledge-Enhanced RAG** in production?\n'
                       '113. What problem or design decision does **Diagnosing Knowledge-Enhanced '
                       'RAG Failures** address in knowledge-enhanced RAG?\n'
                       '114. What is one failure mode or trade-off you would monitor when applying '
                       '**Diagnosing Knowledge-Enhanced RAG Failures** in production?\n'
                       '115. What problem or design decision does **Retain This Idea** address in '
                       'knowledge-enhanced RAG?\n'
                       '116. What is one failure mode or trade-off you would monitor when applying '
                       '**Retain This Idea** in production?\n'
                       '117. Why can a semantically relevant chunk still be insufficient for a '
                       'time-bound question?\n'
                       '118. How would you distinguish a low-recall vector retrieval failure from '
                       'a missing graph relationship?\n'
                       '119. Why are stable entity IDs important when source names change?\n'
                       '120. When would you prefer a graph property over a separate node?\n'
                       '121. Why should relationship direction be modeled explicitly?\n'
                       '122. How can graph provenance improve answer citations?\n'
                       '123. What should happen when an LLM-generated Cypher query references a '
                       'label that is not in the schema?\n'
                       '124. Why is read-only database access a useful control for '
                       'text-to-Cypher?\n'
                       '125. How would you prevent an expensive unbounded graph traversal from '
                       'affecting application latency?\n'
                       '126. Why is chunk enrichment unable to recover evidence that vector search '
                       'never retrieved?\n'
                       '127. When can hybrid graph retrieval justify its higher runtime risk?\n'
                       '128. How can reranking be used after merging vector and graph evidence?\n'
                       '129. What does an orphaned vector record indicate?\n'
                       '130. What does an orphaned graph chunk indicate?\n'
                       '131. Why can duplicate entity nodes silently reduce multi-hop recall?\n'
                       '132. How can deterministic IDs help make graph ingestion idempotent?\n'
                       '133. Why should entity-linking decisions be auditable?\n'
                       '134. What evidence would justify merging two company aliases?\n'
                       '135. When should an ambiguous entity match be sent to human review?\n'
                       '136. Why can a standard ontology reduce long-term maintenance risk?\n'
                       '137. What new dependency is introduced when licensing a curated knowledge '
                       'graph?\n'
                       '138. How does GraphRAG differ from direct graph traversal over a fixed '
                       'ontology?\n'
                       '139. Why are community summaries useful for sensemaking questions?\n'
                       '140. Why can community summaries be unsuitable for legal verbatim '
                       'evidence?\n'
                       '141. How does corpus update frequency affect GraphRAG ROI?\n'
                       '142. Why might local search be preferable to global search for a specific '
                       'entity question?\n'
                       '143. Why can a graph database become memory-bound?\n'
                       '144. How does batching help large graph ingestion?\n'
                       '145. Why is `MERGE` generally safer than blind `CREATE` for restartable '
                       'ingestion?\n'
                       '146. What can go wrong if the graph schema changes but the LLM prompt does '
                       'not?\n'
                       '147. Why can supernodes create unpredictable graph-query latency?\n'
                       '148. How should permissions be enforced before graph evidence reaches the '
                       'LLM?\n'
                       '149. When should a historical relationship be tombstoned rather than '
                       'deleted?\n'
                       '150. What is the difference between CDC and event-driven document '
                       'ingestion?\n'
                       '151. How would you reconcile two entities that are later discovered to be '
                       'identical?\n'
                       '152. Why should KG adoption begin from measured RAG failures rather than '
                       'architectural enthusiasm?\n'
                       '153. What measurements should be compared before and after adding graph '
                       'support?\n'
                       '154. How can a query router reduce the cost of graph-enhanced RAG?\n'
                       '155. Why can standard RAG, KG-hybrid RAG, GraphRAG, and agentic RAG '
                       'coexist in one platform?\n'
                       '156. What is the single most important principle for deciding whether the '
                       'graph’s operational tax is justified?\n'
                       '\n'
                       '\n'
                       '---\n'
                       '\n'
                       '---\n'
                       '\n'
                       '## Final takeaway\n'
                       '\n'
                       'Use a graph when relationships are the problem, not because graphs are '
                       'fashionable. Standard RAG should remain the default when similarity-based '
                       'retrieval already satisfies the evaluation target; add chunk enrichment, '
                       'graph-hybrid retrieval, or GraphRAG only when measured failures justify '
                       'their operational cost.\n',
            'estimated_minutes': 690,
            'has_code_examples': True,
            'has_manual_image_requests': True,
            'sections': [{'id': 'why-knowledge-enhanced-rag',
                          'title': 'Why Knowledge-Enhanced RAG Exists',
                          'order': 1},
                         {'id': 'time-bound-facts',
                          'title': 'Failure Mode 1: Time-Bound Facts',
                          'order': 2},
                         {'id': 'constraint-intersections',
                          'title': 'Failure Mode 2: Intersections of Constraints',
                          'order': 3},
                         {'id': 'multi-hop-reasoning',
                          'title': 'Failure Mode 3: Chained or Multi-Hop Reasoning',
                          'order': 4},
                         {'id': 'kg-overview',
                          'title': 'Knowledge Graphs: The Core Mental Model',
                          'order': 5},
                         {'id': 'nodes-and-properties',
                          'title': 'Nodes, Entities, and Properties',
                          'order': 6},
                         {'id': 'edges-and-relations',
                          'title': 'Edges and Typed Relationships',
                          'order': 7},
                         {'id': 'graph-databases',
                          'title': 'Graph Databases and Why They Exist',
                          'order': 8},
                         {'id': 'cypher-basics',
                          'title': 'Cypher: Reading Graph Patterns',
                          'order': 9},
                         {'id': 'sparql-basics', 'title': 'SPARQL and RDF Triples', 'order': 10},
                         {'id': 'ontology-vs-schema',
                          'title': 'Ontology Versus Schema',
                          'order': 11},
                         {'id': 'movie-kg-design',
                          'title': 'Designing a Movie Knowledge Graph',
                          'order': 12},
                         {'id': 'chunking-scripts',
                          'title': 'Chunking Unstructured Text Before Graph Construction',
                          'order': 13},
                         {'id': 'ner-and-entity-detection',
                          'title': 'Entity Detection Is Domain-Specific',
                          'order': 14},
                         {'id': 'graph-relationships',
                          'title': 'Connecting Chunks to Domain Entities',
                          'order': 15},
                         {'id': 'query-time-patterns',
                          'title': 'Two Main Query-Time Patterns',
                          'order': 16},
                         {'id': 'chunk-enrichment', 'title': 'Chunk Enrichment', 'order': 17},
                         {'id': 'enrichment-advantages',
                          'title': 'Why Chunk Enrichment Is Operationally Attractive',
                          'order': 18},
                         {'id': 'hybrid-graph-retrieval',
                          'title': 'Hybrid-Graph Retrieval',
                          'order': 19},
                         {'id': 'schema-conditioned-query-generation',
                          'title': 'Schema-Conditioned Graph Query Generation',
                          'order': 20},
                         {'id': 'safe-text-to-cypher',
                          'title': 'Making Text-to-Cypher Safer',
                          'order': 21},
                         {'id': 'combine-vector-and-graph',
                          'title': 'Combining Vector and Graph Evidence',
                          'order': 22},
                         {'id': 'choose-enrichment-or-hybrid',
                          'title': 'Choosing Enrichment or Hybrid Retrieval',
                          'order': 23},
                         {'id': 'embedding-location',
                          'title': 'Where Should Embeddings Live?',
                          'order': 24},
                         {'id': 'graph-sync',
                          'title': 'Keeping Vector and Graph Stores Synchronized',
                          'order': 25},
                         {'id': 'building-kgs',
                          'title': 'Building Knowledge Graphs Is the Hard Part',
                          'order': 26},
                         {'id': 'automated-kg-construction',
                          'title': 'Automating KG Construction from Text',
                          'order': 27},
                         {'id': 'entity-identification',
                          'title': 'Entity Identification',
                          'order': 28},
                         {'id': 'relation-extraction', 'title': 'Relation Extraction', 'order': 29},
                         {'id': 'entity-linking',
                          'title': 'Entity Linking: One Thing, Many Names',
                          'order': 30},
                         {'id': 'ontology-for-linking',
                          'title': 'Using an Ontology to Guide Entity Linking',
                          'order': 31},
                         {'id': 'normalization-and-candidates',
                          'title': 'Normalization and Candidate Generation',
                          'order': 32},
                         {'id': 'human-in-loop-linking',
                          'title': 'Human-in-the-Loop Entity Resolution',
                          'order': 33},
                         {'id': 'standard-ontologies',
                          'title': 'Leveraging Standard Ontologies',
                          'order': 34},
                         {'id': 'licensed-kgs',
                          'title': 'Leveraging Curated or Licensed Knowledge Graphs',
                          'order': 35},
                         {'id': 'graphrag-definition',
                          'title': 'Microsoft GraphRAG: A Different Use of Graphs',
                          'order': 36},
                         {'id': 'graphrag-indexing',
                          'title': 'GraphRAG Indexing Pipeline',
                          'order': 37},
                         {'id': 'community-detection',
                          'title': 'Community Detection and Hierarchical Summaries',
                          'order': 38},
                         {'id': 'local-vs-global-search',
                          'title': 'GraphRAG Local Search Versus Global Search',
                          'order': 39},
                         {'id': 'graphrag-cost', 'title': 'The Cost of GraphRAG', 'order': 40},
                         {'id': 'when-graphrag-is-wrong',
                          'title': 'When GraphRAG Is the Wrong Tool',
                          'order': 41},
                         {'id': 'graph-infrastructure',
                          'title': 'Graph Database Infrastructure Is a Long-Term Commitment',
                          'order': 42},
                         {'id': 'graph-deployment-models',
                          'title': 'Graph Deployment Models',
                          'order': 43},
                         {'id': 'kg-etl',
                          'title': 'Knowledge-Graph ETL and Idempotency',
                          'order': 44},
                         {'id': 'schema-evolution', 'title': 'Schema Evolution', 'order': 45},
                         {'id': 'graph-performance',
                          'title': 'Graph Performance and Supernodes',
                          'order': 46},
                         {'id': 'graph-security',
                          'title': 'Security, Backup, and High Availability',
                          'order': 47},
                         {'id': 'living-graph', 'title': 'Maintaining a Living Graph', 'order': 48},
                         {'id': 'cdc-vs-events',
                          'title': 'CDC Versus Event-Driven Graph Updates',
                          'order': 49},
                         {'id': 'entity-merges', 'title': 'Handling Entity Merges', 'order': 50},
                         {'id': 'fact-lifecycle',
                          'title': 'Fact Lifecycle and Tombstoning',
                          'order': 51},
                         {'id': 'accuracy-cost-tradeoff',
                          'title': 'The Accuracy–Cost Trade-Off',
                          'order': 52},
                         {'id': 'kg-roi-checklist',
                          'title': 'A Practical KG ROI Checklist',
                          'order': 53},
                         {'id': 'architecture-comparison',
                          'title': 'Comparing RAG Architectures',
                          'order': 54},
                         {'id': 'evaluation-driven-adoption',
                          'title': 'Use Evaluation to Decide When to Add a Graph',
                          'order': 55},
                         {'id': 'production-blueprint',
                          'title': 'Production Blueprint for Knowledge-Enhanced RAG',
                          'order': 56},
                         {'id': 'diagnosing-failures',
                          'title': 'Diagnosing Knowledge-Enhanced RAG Failures',
                          'order': 57},
                         {'id': 'common-misconceptions',
                          'title': 'Common Misconceptions',
                          'order': 58},
                         {'id': 'terminology-reference',
                          'title': 'Terminology Reference',
                          'order': 59},
                         {'id': 'retain-mental-model',
                          'title': 'Retain This Mental Model',
                          'order': 60}]},
 'exercises': [{'id': 'M01.L09.EX01',
                'title': 'Classify the Retrieval Failure',
                'lesson_code': 'M01.L09',
                'section_id': 'multi-hop-reasoning',
                'placement': 'after_section',
                'description': 'Given three queries, classify whether standard semantic retrieval '
                               'is likely sufficient or whether explicit graph relationships are '
                               'needed.',
                'instructions': 'For each query, identify whether the answer depends on semantic '
                                'similarity, exact constraints, temporal validity, or traversal '
                                'across relationships. Route it to standard/hybrid RAG or a '
                                'graph-enhanced path and explain why.',
                'expected_output': 'A classification table with query type, chosen retrieval path, '
                                   'and the failure mode avoided.',
                'skill_tested': ['retrieval-diagnosis', 'knowledge-graphs'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX02',
                'title': 'Model a Small Knowledge Graph',
                'lesson_code': 'M01.L09',
                'section_id': 'kg-overview',
                'placement': 'after_section',
                'description': 'Design nodes, properties, and typed relationships for a university '
                               'course-prerequisite domain.',
                'instructions': 'Model courses, students, departments, and prerequisites. Define '
                                'at least four node types or labels, five relationship types, key '
                                'properties, and one relationship direction constraint.',
                'expected_output': 'A compact university KG design showing entities, properties, '
                                   'typed edges, and one example path query.',
                'skill_tested': ['knowledge-graphs', 'data-modeling'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX03',
                'title': 'Read a Cypher Pattern',
                'lesson_code': 'M01.L09',
                'section_id': 'cypher-basics',
                'placement': 'after_section',
                'description': 'Explain in plain language what a supplied Person-DIRECTED-Movie '
                               'Cypher pattern retrieves, then modify the filter to select a '
                               'release year.',
                'instructions': 'Translate the MATCH pattern into plain English, then add a '
                                'release-year filter and return both director and movie title. '
                                'Explain how directionality affects the match.',
                'expected_output': 'A plain-language interpretation plus a corrected Cypher query '
                                   'with the added year constraint.',
                'skill_tested': ['cypher', 'graph-querying'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX04',
                'title': 'Translate a Triple Pattern',
                'lesson_code': 'M01.L09',
                'section_id': 'sparql-basics',
                'placement': 'after_section',
                'description': 'Represent a simple director-movie fact as RDF-style '
                               'subject-predicate-object triples and explain the query variables.',
                'instructions': 'Write RDF-style triples for a person directing a movie and the '
                                'movie having a title. Then write a SPARQL WHERE block that binds '
                                'the person name as an output variable.',
                'expected_output': 'A set of subject-predicate-object triples and a small SPARQL '
                                   'pattern using variables correctly.',
                'skill_tested': ['sparql', 'rdf'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX05',
                'title': 'Separate Ontology from Schema',
                'lesson_code': 'M01.L09',
                'section_id': 'ontology-vs-schema',
                'placement': 'after_section',
                'description': 'For a product domain, write two ontology rules and show how each '
                               'becomes a concrete graph schema element.',
                'instructions': 'Define two domain-level truths independent of storage, then '
                                'implement each as labels/properties/relationship constraints in a '
                                'concrete graph schema.',
                'expected_output': 'Two ontology rules paired with their database-schema '
                                   'implementation.',
                'skill_tested': ['ontology', 'schema'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX06',
                'title': 'Design Stable Chunk Identity',
                'lesson_code': 'M01.L09',
                'section_id': 'chunking-scripts',
                'placement': 'after_section',
                'description': 'Specify the identifiers and metadata needed to join a chunk stored '
                               'in a vector DB with the same chunk represented in a graph.',
                'instructions': 'Specify source_document_id, chunk_id, version, checksum, '
                                'offsets/page, and graph-node ID. Explain how these fields let you '
                                'detect stale or orphaned representations across stores.',
                'expected_output': 'A stable chunk identity contract and two integrity checks '
                                   'between vector and graph systems.',
                'skill_tested': ['chunk-identity', 'data-integrity'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX07',
                'title': 'Enrich a Retrieved Chunk',
                'lesson_code': 'M01.L09',
                'section_id': 'chunk-enrichment',
                'placement': 'after_section',
                'description': 'Take a thin chunk that mentions only a character name and design '
                               'the graph lookups required to add actor and movie context.',
                'instructions': 'Identify the entity mention in the thin chunk, list the graph '
                                'traversals required to reach actor and movie facts, then show the '
                                'enriched context packet supplied to generation.',
                'expected_output': 'A traversal plan and enriched chunk containing both original '
                                   'text and graph-derived facts with provenance.',
                'skill_tested': ['chunk-enrichment', 'graph-rag'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX08',
                'title': 'Choose Enrichment or Hybrid Retrieval',
                'lesson_code': 'M01.L09',
                'section_id': 'choose-enrichment-or-hybrid',
                'placement': 'after_section',
                'description': 'For four query types, choose chunk enrichment or hybrid graph '
                               'retrieval and justify the choice.',
                'instructions': 'Classify quote lookup, entity metadata lookup, multi-hop '
                                'relationship discovery, and aggregate relationship queries. '
                                'Explain why enrichment or graph-first discovery is the lower-risk '
                                'choice in each case.',
                'expected_output': 'Four routing decisions with latency, reliability, and '
                                   'reasoning-complexity justification.',
                'skill_tested': ['graph-rag', 'architecture'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX09',
                'title': 'Guard a Text-to-Cypher Pipeline',
                'lesson_code': 'M01.L09',
                'section_id': 'safe-text-to-cypher',
                'placement': 'after_section',
                'description': 'Design a safety layer for LLM-generated Cypher including '
                               'permissions, validation, timeout, and result limits.',
                'instructions': 'Constrain the LLM to a read-only graph schema, validate generated '
                                'syntax/labels, enforce parameterization, add timeout/result '
                                'limits, and define retry/fallback behavior for rejected queries.',
                'expected_output': 'A guarded text-to-Cypher execution pipeline with controls '
                                   'before and during database execution.',
                'skill_tested': ['text-to-cypher', 'security'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX10',
                'title': 'Reconcile Vector and Graph Stores',
                'lesson_code': 'M01.L09',
                'section_id': 'graph-sync',
                'placement': 'after_section',
                'description': 'Design a nightly integrity check that detects orphaned chunks and '
                               'version mismatches between a vector index and graph DB.',
                'instructions': 'Compare chunk IDs, document versions, checksums, and deletion '
                                'status across both systems. Define alerts and repair actions for '
                                'vector-only and graph-only chunks.',
                'expected_output': 'A reconciliation job specification with mismatch classes and '
                                   'remediation actions.',
                'skill_tested': ['vector-graph-sync', 'data-integrity'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX11',
                'title': 'Resolve Entity Aliases',
                'lesson_code': 'M01.L09',
                'section_id': 'entity-linking',
                'placement': 'after_section',
                'description': 'Given aliases for a company, drug, and product, propose canonical '
                               'records and the evidence needed before merging.',
                'instructions': 'Normalize each alias set, generate candidate matches, evaluate '
                                'contextual/domain evidence, and define the confidence required '
                                'for automatic merge versus human review.',
                'expected_output': 'Three canonical entity records with alias mappings, confidence '
                                   'evidence, and merge/review decisions.',
                'skill_tested': ['entity-linking', 'data-quality'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX12',
                'title': 'Design an Entity-Linking Review Queue',
                'lesson_code': 'M01.L09',
                'section_id': 'human-in-loop-linking',
                'placement': 'after_section',
                'description': 'Define confidence thresholds and what information a reviewer '
                               'should see for ambiguous entity matches.',
                'instructions': 'Define high-confidence auto-merge, medium-confidence review, and '
                                'low-confidence reject thresholds. Specify the source text, '
                                'candidate entities, conflicting attributes, and provenance a '
                                'reviewer needs.',
                'expected_output': 'A triage policy and reviewer payload for ambiguous entity '
                                   'linking.',
                'skill_tested': ['human-in-the-loop', 'entity-resolution'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX13',
                'title': 'Choose Local or Global GraphRAG Search',
                'lesson_code': 'M01.L09',
                'section_id': 'local-vs-global-search',
                'placement': 'after_section',
                'description': 'Classify a set of detailed and sensemaking queries as local or '
                               'global GraphRAG search and explain why.',
                'instructions': 'Route entity-neighborhood questions to local search and '
                                'corpus-wide theme/sensemaking questions to global search. Explain '
                                'which graph artifacts each path relies on.',
                'expected_output': 'A query-routing table distinguishing local neighborhood '
                                   'retrieval from community-summary synthesis.',
                'skill_tested': ['graphrag', 'query-routing'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX14',
                'title': 'Estimate GraphRAG Suitability',
                'lesson_code': 'M01.L09',
                'section_id': 'when-graphrag-is-wrong',
                'placement': 'after_section',
                'description': 'Evaluate whether GraphRAG fits a rapidly changing support-ticket '
                               'corpus and propose an alternative architecture.',
                'instructions': 'Assess update frequency, need for verbatim evidence, '
                                'response-latency target, corpus size, and dominant query type. '
                                'Then choose standard RAG, KG-hybrid, or GraphRAG.',
                'expected_output': 'A suitability assessment showing why GraphRAG is or is not '
                                   'appropriate and a lower-cost alternative when rejected.',
                'skill_tested': ['graphrag', 'architecture'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX15',
                'title': 'Make KG Ingestion Restartable',
                'lesson_code': 'M01.L09',
                'section_id': 'kg-etl',
                'placement': 'after_section',
                'description': 'Design an idempotent batched ingestion workflow that can resume '
                               'after a failure without duplicating graph entities.',
                'instructions': 'Use canonical IDs and MERGE semantics, process bounded batches, '
                                'checkpoint each batch, and make retries safe after partial '
                                'failure. Explain how duplicate creation is prevented.',
                'expected_output': 'A restartable KG ingestion sequence with idempotency keys, '
                                   'batching, checkpoints, and retry behavior.',
                'skill_tested': ['kg-etl', 'idempotency'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX16',
                'title': 'Design a Living-Graph Update Flow',
                'lesson_code': 'M01.L09',
                'section_id': 'cdc-vs-events',
                'placement': 'after_section',
                'description': 'Choose CDC or event-driven updates for three source systems and '
                               'describe how deletes and updates propagate.',
                'instructions': 'For Postgres, uploaded PDFs, and application events, choose CDC '
                                'or event-driven updates. Specify create/update/delete mapping '
                                'into the graph and how entity versions are maintained.',
                'expected_output': 'Three source-specific update flows including propagation of '
                                   'updates and deletions.',
                'skill_tested': ['cdc', 'event-driven'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX17',
                'title': 'Run the KG ROI Checklist',
                'lesson_code': 'M01.L09',
                'section_id': 'kg-roi-checklist',
                'placement': 'after_section',
                'description': "Apply the chapter's ROI criteria to a hypothetical compliance "
                               'assistant and decide whether a graph pilot is justified.',
                'instructions': 'Score the compliance assistant against recurring graph-worthy '
                                'failures, deterministic grounding needs, available ontology '
                                'assets, data connectivity, team ownership, and measurable '
                                'business ROI.',
                'expected_output': 'A completed ROI checklist with a justified pilot/no-pilot '
                                   'decision and success metrics.',
                'skill_tested': ['knowledge-graphs', 'roi'],
                'difficulty': 'intermediate'},
               {'id': 'M01.L09.EX18',
                'title': 'Diagnose a Graph-Augmented Failure',
                'lesson_code': 'M01.L09',
                'section_id': 'diagnosing-failures',
                'placement': 'after_section',
                'description': 'Trace a wrong answer through graph construction, entity linking, '
                               'query generation, retrieval merge, and generation to identify the '
                               'most likely failing layer.',
                'instructions': 'Trace the answer backward through generation, merged evidence, '
                                'graph query, entity linking, relation extraction, and source '
                                'ingestion. Identify what logs or graph inspections would confirm '
                                'each hypothesis.',
                'expected_output': 'A root-cause debugging plan that isolates the most likely '
                                   'failing layer with observable evidence.',
                'skill_tested': ['observability', 'graph-rag'],
                'difficulty': 'intermediate'}],
 'quiz': {'id': 'M01.L09.QUIZ',
          'title': 'Knowledge-Enhanced RAG — Lesson Quiz',
          'lesson_code': 'M01.L09',
          'placement': 'lesson_end',
          'questions': [{'id': 'M01.L09.Q01',
                         'type': 'multiple_choice',
                         'section_id': 'multi-hop-reasoning',
                         'question': 'Which retrieval problem most strongly motivates adding '
                                     'explicit graph relationships?',
                         'options': ['Finding text with similar wording',
                                     'Following a chain of typed relationships across several '
                                     'entities',
                                     'Reducing token count in a prompt',
                                     'Splitting a document into chunks'],
                         'correct': 1,
                         'explanation': 'Multi-hop questions depend on relationship paths, not '
                                        'only semantic similarity.'},
                        {'id': 'M01.L09.Q02',
                         'type': 'multiple_choice',
                         'section_id': 'kg-overview',
                         'question': 'What does a knowledge graph add that vector similarity alone '
                                     'does not guarantee?',
                         'options': ['Typed, explicit relationships among entities',
                                     'Lower embedding dimensions',
                                     'Automatic OCR',
                                     'A larger context window'],
                         'correct': 0,
                         'explanation': 'Graphs encode explicit structure that can be traversed '
                                        'deterministically.'},
                        {'id': 'M01.L09.Q03',
                         'type': 'multiple_choice',
                         'section_id': 'cypher-basics',
                         'question': 'In `(p:Person)-[:DIRECTED]->(m:Movie)`, what does `DIRECTED` '
                                     'represent?',
                         'options': ['A node label',
                                     'A property value',
                                     'A typed relationship',
                                     'A vector index'],
                         'correct': 2,
                         'explanation': 'Square-bracketed `DIRECTED` is the relationship type '
                                        'connecting the nodes.'},
                        {'id': 'M01.L09.Q04',
                         'type': 'multiple_choice',
                         'section_id': 'sparql-basics',
                         'question': 'What is the basic data unit queried by SPARQL?',
                         'options': ['A tensor',
                                     'A subject-predicate-object triple',
                                     'A chunk overlap',
                                     'A SQL row only'],
                         'correct': 1,
                         'explanation': 'RDF graphs express knowledge as triples.'},
                        {'id': 'M01.L09.Q05',
                         'type': 'multiple_choice',
                         'section_id': 'ontology-vs-schema',
                         'question': 'Which statement best distinguishes an ontology from a '
                                     'schema?',
                         'options': ['An ontology models domain concepts and rules; a schema '
                                     'implements them in the database',
                                     'A schema is broader and more abstract than an ontology',
                                     'They are always identical',
                                     'An ontology stores embeddings while a schema stores text'],
                         'correct': 0,
                         'explanation': 'The ontology is the conceptual model; the schema is its '
                                        'concrete database representation.'},
                        {'id': 'M01.L09.Q06',
                         'type': 'multiple_choice',
                         'section_id': 'chunk-enrichment',
                         'question': 'What is the main purpose of chunk enrichment?',
                         'options': ['Replace vector retrieval completely',
                                     'Add graph-derived structured context to an already relevant '
                                     'retrieved chunk',
                                     'Delete metadata before generation',
                                     'Create community summaries'],
                         'correct': 1,
                         'explanation': 'Enrichment starts from a retrieved chunk and adds missing '
                                        'structured facts.'},
                        {'id': 'M01.L09.Q07',
                         'type': 'multiple_choice',
                         'section_id': 'hybrid-graph-retrieval',
                         'question': 'What new failure surface appears in hybrid graph retrieval?',
                         'options': ['Text-to-Cypher or text-to-SPARQL generation can be invalid '
                                     'or unsafe',
                                     'Cosine similarity becomes impossible',
                                     'Chunks can no longer be cited',
                                     'Graph databases cannot store strings'],
                         'correct': 0,
                         'explanation': 'LLM-generated graph queries require validation and '
                                        'execution guardrails.'},
                        {'id': 'M01.L09.Q08',
                         'type': 'multiple_choice',
                         'section_id': 'safe-text-to-cypher',
                         'question': 'Which control most directly limits damage from a bad '
                                     'LLM-generated graph query?',
                         'options': ['Write access to every graph node',
                                     'Read-only credentials plus timeouts and result limits',
                                     'Removing the graph schema from the prompt',
                                     'Increasing temperature'],
                         'correct': 1,
                         'explanation': 'Least privilege and bounded execution reduce the risk of '
                                        'generated queries.'},
                        {'id': 'M01.L09.Q09',
                         'type': 'multiple_choice',
                         'section_id': 'graph-sync',
                         'question': 'What is the main risk of keeping vectors and graph data in '
                                     'separate stores?',
                         'options': ['The need to synchronize chunk identity, versions, inserts, '
                                     'updates, and deletes',
                                     'Cypher stops working',
                                     'Embeddings become text',
                                     'The graph cannot have properties'],
                         'correct': 0,
                         'explanation': 'Separate stores create a consistency obligation.'},
                        {'id': 'M01.L09.Q10',
                         'type': 'multiple_choice',
                         'section_id': 'entity-linking',
                         'question': 'What problem does entity linking solve?',
                         'options': ['Choosing chunk size',
                                     'Mapping multiple aliases or mentions to one canonical '
                                     'real-world entity',
                                     'Selecting an LLM temperature',
                                     'Compressing images'],
                         'correct': 1,
                         'explanation': 'Entity linking prevents one real-world thing from '
                                        'fragmenting into duplicate graph nodes.'},
                        {'id': 'M01.L09.Q11',
                         'type': 'multiple_choice',
                         'section_id': 'graphrag-definition',
                         'question': 'What is Microsoft GraphRAG primarily designed to improve?',
                         'options': ['Broad sensemaking and query-focused summarization over a '
                                     'corpus',
                                     'Exact keyword search only',
                                     'Speech diarization',
                                     'PDF OCR'],
                         'correct': 0,
                         'explanation': 'GraphRAG builds graph communities and summaries to answer '
                                        'broad corpus-level questions.'},
                        {'id': 'M01.L09.Q12',
                         'type': 'multiple_choice',
                         'section_id': 'local-vs-global-search',
                         'question': 'Which GraphRAG mode is better suited to broad themes across '
                                     'many documents?',
                         'options': ['Local search',
                                     'Global search',
                                     'BM25 only',
                                     'Exact nearest neighbor'],
                         'correct': 1,
                         'explanation': 'Global search uses broad community-level information for '
                                        'corpus-wide synthesis.'},
                        {'id': 'M01.L09.Q13',
                         'type': 'multiple_choice',
                         'section_id': 'when-graphrag-is-wrong',
                         'question': 'Which workload is a poor fit for GraphRAG?',
                         'options': ['A broad theme-analysis task over a stable corpus',
                                     'A rapidly changing corpus that requires fresh, verbatim '
                                     'evidence',
                                     'A sensemaking query',
                                     'A corpus where community summaries are valuable'],
                         'correct': 1,
                         'explanation': 'Frequent updates and strict verbatim evidence make '
                                        "GraphRAG's preprocessing and abstraction costly."},
                        {'id': 'M01.L09.Q14',
                         'type': 'multiple_choice',
                         'section_id': 'kg-etl',
                         'question': 'Why is idempotency important in graph ingestion?',
                         'options': ['It makes reruns safe after partial failure',
                                     'It guarantees zero latency',
                                     'It removes the need for entity IDs',
                                     'It replaces backups'],
                         'correct': 0,
                         'explanation': 'Idempotent operations can be retried without duplicating '
                                        'or corrupting the graph.'},
                        {'id': 'M01.L09.Q15',
                         'type': 'multiple_choice',
                         'section_id': 'schema-evolution',
                         'question': 'Why should graph schema changes be versioned?',
                         'options': ["Because the LLM's query-generation logic depends on the "
                                     'current labels, relationships, and properties',
                                     'Because graphs cannot change',
                                     'Because embeddings require SQL',
                                     'Because versioning eliminates ETL'],
                         'correct': 0,
                         'explanation': 'Query generation must remain synchronized with the graph '
                                        'structure.'},
                        {'id': 'M01.L09.Q16',
                         'type': 'multiple_choice',
                         'section_id': 'cdc-vs-events',
                         'question': 'Which update pattern best fits row-level changes in a '
                                     'transactional database?',
                         'options': ['Change data capture',
                                     'Manual full rebuild only',
                                     'Image captioning',
                                     'Community detection'],
                         'correct': 0,
                         'explanation': 'CDC observes structured source-database changes and '
                                        'propagates them downstream.'},
                        {'id': 'M01.L09.Q17',
                         'type': 'multiple_choice',
                         'section_id': 'kg-roi-checklist',
                         'question': 'What should justify the operational cost of adding a '
                                     'knowledge graph?',
                         'options': ['Architecture fashion',
                                     'Measured accuracy gains on important failure modes tied to '
                                     'business value',
                                     'The existence of a graph library',
                                     'A desire to maximize system components'],
                         'correct': 1,
                         'explanation': 'The graph should earn its cost through measurable '
                                        'improvement on meaningful queries.'},
                        {'id': 'M01.L09.Q18',
                         'type': 'multiple_choice',
                         'section_id': 'retain-mental-model',
                         'question': 'Which principle best summarizes the lesson?',
                         'options': ['Always replace RAG with a graph',
                                     'Use the simplest retrieval architecture that reliably '
                                     'answers the real query class',
                                     'GraphRAG is always cheaper than vector search',
                                     'Agents and graphs solve exactly the same problem'],
                         'correct': 1,
                         'explanation': 'Architecture should match the question structure and '
                                        'required quality, latency, and cost.'}],
          'passing_score': 70}}
