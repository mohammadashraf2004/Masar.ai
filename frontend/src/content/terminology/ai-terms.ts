/**
 * Canonical AI/ML technical terminology dictionary.
 *
 * This is the single source of truth for the Arabic-first content policy:
 * explanations are written in Arabic, but the *terminology* a student will
 * meet on GitHub, Stack Overflow, in papers and in job descriptions stays
 * in English. `preferred` is the form we keep using in prose after the
 * first mention; `ar` exists to explain the term once, not to replace it.
 *
 * The backend keeps a generated copy at `backend/app/content/ai_terms.json`
 * (used for bilingual search, the AI tutor's language policy, and the
 * content linter). After editing this file run:
 *
 *     npm run terminology:export
 *
 * See docs/content/ARABIC_FIRST_GUIDELINES.md before adding terms.
 */

export type TermCategory =
  | 'LLM'
  | 'RAG'
  | 'Agents'
  | 'Training'
  | 'Serving'
  | 'Data'
  | 'Engineering'
  | 'Evaluation'

export type TermLevel = 'beginner' | 'intermediate' | 'advanced'

export interface TechnicalTermEntry {
  /** Stable snake_case key — used by vocabulary progress, never displayed. */
  id: string
  /** Full English industry term. */
  en: string
  /** Arabic meaning. Explains the term once; does not replace `preferred`. */
  ar: string
  /** The form used in running prose (usually `en`, or the abbreviation). */
  preferred: string
  abbreviation?: string
  category: TermCategory
  level: TermLevel
  /** Extra surface forms, any language — feeds search and in-lesson detection. */
  aliases?: string[]
  definitionAr: string
  definitionEn: string
  /** Short concrete illustration: Arabic prose, English terminology. */
  exampleAr?: string
}

export const AI_TERMS: Record<string, TechnicalTermEntry> = {
  // ── LLM fundamentals ──────────────────────────────────────────────────
  large_language_model: {
    id: 'large_language_model',
    en: 'Large Language Model',
    ar: 'نموذج لغوي كبير',
    preferred: 'LLM',
    abbreviation: 'LLM',
    category: 'LLM',
    level: 'beginner',
    aliases: ['llm', 'llms', 'language model', 'نموذج لغوي', 'النماذج اللغوية'],
    definitionAr:
      'نموذج تم تدريبه على كميات ضخمة من النصوص ليتنبأ بالـ token التالي، وهو الأساس الذي تُبنى عليه معظم تطبيقات الـ Generative AI.',
    definitionEn:
      'A model trained on large text corpora to predict the next token; the foundation of most generative AI applications.',
    exampleAr: 'GPT و Claude و Gemini كلها أمثلة على LLM.',
  },
  transformer: {
    id: 'transformer',
    en: 'Transformer',
    ar: 'المحول',
    preferred: 'Transformer',
    category: 'LLM',
    level: 'intermediate',
    aliases: ['transformers', 'المحولات'],
    definitionAr:
      'الـ architecture الذي تقوم عليه معظم الـ LLMs، ويعتمد على الـ Attention بدل المعالجة المتسلسلة، فيعالج الجملة كاملة بالتوازي.',
    definitionEn:
      'The neural network architecture behind most LLMs, built on attention instead of sequential recurrence.',
  },
  attention: {
    id: 'attention',
    en: 'Attention',
    ar: 'الانتباه',
    preferred: 'Attention',
    category: 'LLM',
    level: 'intermediate',
    aliases: ['self-attention', 'self attention', 'الانتباه الذاتي'],
    definitionAr:
      'آلية تسمح للنموذج بتحديد أي أجزاء الـ input أكثر ارتباطاً بالـ token الذي يعالجه الآن، فيعطيها وزناً أكبر.',
    definitionEn:
      'A mechanism that lets the model weigh which parts of the input matter most for the token it is currently processing.',
  },
  token: {
    id: 'token',
    en: 'Token',
    ar: 'وحدة نصية',
    preferred: 'Token',
    category: 'LLM',
    level: 'beginner',
    aliases: ['tokens', 'التوكن', 'التوكنز'],
    definitionAr:
      'أصغر وحدة يتعامل معها النموذج، وقد تكون كلمة أو جزءاً من كلمة. التكلفة والـ Context Window يُحسبان بالـ tokens لا بالكلمات.',
    definitionEn:
      'The smallest unit an LLM processes — a word or a word fragment. Both cost and context limits are measured in tokens.',
  },
  tokenizer: {
    id: 'tokenizer',
    en: 'Tokenizer',
    ar: 'المُجزِّئ',
    preferred: 'Tokenizer',
    category: 'LLM',
    level: 'intermediate',
    aliases: ['tokenization', 'tokenizing'],
    definitionAr: 'المكوّن الذي يحوّل النص إلى tokens قبل دخوله للنموذج، ويعيدها نصاً بعد الخروج.',
    definitionEn:
      'The component that converts text into tokens before the model sees it, and back to text afterwards.',
  },
  context_window: {
    id: 'context_window',
    en: 'Context Window',
    ar: 'نافذة السياق',
    preferred: 'Context Window',
    category: 'LLM',
    level: 'beginner',
    aliases: ['context length', 'context size'],
    definitionAr:
      'الحد الأقصى لعدد الـ tokens التي يستطيع النموذج رؤيتها في الطلب الواحد، شاملة الـ prompt والإجابة معاً.',
    definitionEn:
      'The maximum number of tokens a model can attend to in one request, prompt and completion combined.',
  },
  prompt: {
    id: 'prompt',
    en: 'Prompt',
    ar: 'الأمر النصي',
    preferred: 'Prompt',
    category: 'LLM',
    level: 'beginner',
    aliases: ['prompts', 'البرومبت'],
    definitionAr: 'النص الذي ترسله للنموذج ليعمل عليه: التعليمات والسياق والسؤال.',
    definitionEn: 'The input text you send to a model: instructions, context, and the question.',
  },
  prompt_engineering: {
    id: 'prompt_engineering',
    en: 'Prompt Engineering',
    ar: 'هندسة الأوامر',
    preferred: 'Prompt Engineering',
    category: 'LLM',
    level: 'beginner',
    aliases: ['prompting', 'هندسة البرومبت'],
    definitionAr:
      'صياغة الـ prompt بشكل منهجي — تعليمات واضحة، أمثلة، وتحديد شكل الإخراج — للحصول على نتائج ثابتة وقابلة للتكرار.',
    definitionEn:
      'Systematically designing prompts — clear instructions, examples, output format — to get reliable, repeatable results.',
  },
  system_prompt: {
    id: 'system_prompt',
    en: 'System Prompt',
    ar: 'أمر النظام',
    preferred: 'System Prompt',
    category: 'LLM',
    level: 'beginner',
    aliases: ['system message', 'system instructions'],
    definitionAr:
      'تعليمات ثابتة تُحدّد دور النموذج وسلوكه، وتُرسل قبل رسائل المستخدم في كل طلب.',
    definitionEn:
      "Persistent instructions that define the model's role and behaviour, sent ahead of the user's messages.",
  },
  few_shot: {
    id: 'few_shot',
    en: 'Few-shot Prompting',
    ar: 'التلقين بأمثلة قليلة',
    preferred: 'Few-shot',
    category: 'LLM',
    level: 'intermediate',
    aliases: ['few shot', 'zero-shot', 'zero shot', 'in-context learning'],
    definitionAr:
      'وضع عدة أمثلة داخل الـ prompt ليستنتج النموذج النمط المطلوب، بدل إعادة تدريبه.',
    definitionEn:
      'Placing a handful of examples inside the prompt so the model infers the pattern, instead of retraining it.',
  },
  chain_of_thought: {
    id: 'chain_of_thought',
    en: 'Chain-of-Thought',
    ar: 'سلسلة التفكير',
    preferred: 'Chain-of-Thought',
    abbreviation: 'CoT',
    category: 'LLM',
    level: 'intermediate',
    aliases: ['cot', 'chain of thought', 'reasoning steps'],
    definitionAr:
      'أسلوب يطلب من النموذج عرض خطوات تفكيره قبل الإجابة النهائية، ويحسّن الدقة في المسائل متعددة الخطوات.',
    definitionEn:
      'Prompting the model to lay out intermediate reasoning steps before its final answer, improving accuracy on multi-step problems.',
  },
  temperature: {
    id: 'temperature',
    en: 'Temperature',
    ar: 'درجة العشوائية',
    preferred: 'Temperature',
    category: 'LLM',
    level: 'beginner',
    aliases: ['top_p', 'top-p', 'sampling'],
    definitionAr:
      'مُعامل يتحكم في عشوائية الإخراج: القيمة المنخفضة تعطي إجابات ثابتة، والمرتفعة تعطي تنوعاً أكبر.',
    definitionEn:
      'A sampling parameter controlling output randomness: low values give deterministic answers, high values more variety.',
  },
  hallucination: {
    id: 'hallucination',
    en: 'Hallucination',
    ar: 'الهلوسة',
    preferred: 'Hallucination',
    category: 'LLM',
    level: 'beginner',
    aliases: ['hallucinations', 'hallucinate'],
    definitionAr:
      'أن يُنتج النموذج معلومة تبدو مقنعة لكنها غير صحيحة أو غير موجودة في مصادره. الـ RAG والـ Grounding من أهم وسائل تقليلها.',
    definitionEn:
      'When a model produces confident but false or unsupported information. RAG and grounding are the standard mitigations.',
  },
  structured_output: {
    id: 'structured_output',
    en: 'Structured Output',
    ar: 'الإخراج المنظم',
    preferred: 'Structured Output',
    category: 'LLM',
    level: 'intermediate',
    aliases: ['json mode', 'json_mode', 'response format', 'schema output'],
    definitionAr:
      'إجبار النموذج على الرد بصيغة محدّدة (JSON غالباً) مطابقة لـ schema، حتى يتعامل الكود مع الرد مباشرة بدل تحليل نص حر.',
    definitionEn:
      'Constraining a model to answer in a fixed machine-readable format (usually JSON matching a schema) so code can consume it directly.',
  },
  prompt_injection: {
    id: 'prompt_injection',
    en: 'Prompt Injection',
    ar: 'حقن الأوامر',
    preferred: 'Prompt Injection',
    category: 'LLM',
    level: 'advanced',
    aliases: ['jailbreak', 'حقن البرومبت'],
    definitionAr:
      'هجوم يضع فيه المهاجم تعليمات داخل محتوى يقرأه النموذج (مستند أو صفحة ويب) ليتجاوز تعليماتك الأصلية.',
    definitionEn:
      'An attack where instructions hidden in content the model reads override the developer’s original instructions.',
  },

  // ── RAG ───────────────────────────────────────────────────────────────
  embeddings: {
    id: 'embeddings',
    en: 'Embeddings',
    ar: 'التضمينات',
    preferred: 'Embeddings',
    category: 'RAG',
    level: 'beginner',
    aliases: ['embedding', 'embed', 'التضمين', 'تمثيل النصوص', 'تمثيلات رقمية'],
    definitionAr:
      'تمثيلات رقمية للنصوص أو البيانات في صورة vectors، بحيث تقع المعاني المتقاربة قريبة من بعضها، فيمكن قياس مدى التشابه بينها.',
    definitionEn:
      'Numerical representations of text or data as vectors, where semantically similar items land close together so similarity can be measured.',
    exampleAr: '"machine learning" و "AI" لهما embeddings متقاربة لأن معناهما مترابط.',
  },
  vector: {
    id: 'vector',
    en: 'Vector',
    ar: 'متجه',
    preferred: 'Vector',
    category: 'RAG',
    level: 'beginner',
    aliases: ['vectors', 'المتجهات', 'متجهات'],
    definitionAr: 'قائمة من الأرقام تمثل عنصراً واحداً (نص، صورة، صوت) في فضاء متعدد الأبعاد.',
    definitionEn:
      'An ordered list of numbers representing one item (text, image, audio) in a high-dimensional space.',
  },
  vector_database: {
    id: 'vector_database',
    en: 'Vector Database',
    ar: 'قاعدة بيانات المتجهات',
    preferred: 'Vector Database',
    category: 'RAG',
    level: 'beginner',
    aliases: ['vector db', 'vectordb', 'vector store', 'vector index', 'قاعدة بيانات متجهية'],
    definitionAr:
      'قاعدة بيانات مُحسَّنة لتخزين الـ embeddings والبحث فيها بالتشابه بدل المطابقة الحرفية. أمثلة: Qdrant و Chroma و FAISS و pgvector.',
    definitionEn:
      'A database optimised for storing embeddings and searching them by similarity rather than exact match — Qdrant, Chroma, FAISS, pgvector.',
  },
  semantic_search: {
    id: 'semantic_search',
    en: 'Semantic Search',
    ar: 'البحث الدلالي',
    preferred: 'Semantic Search',
    category: 'RAG',
    level: 'beginner',
    aliases: ['similarity search', 'vector search', 'البحث بالمعنى', 'بحث دلالي'],
    definitionAr:
      'البحث بالمعنى لا بالكلمة: نحوّل الـ query إلى embedding ونجلب أقرب vectors إليه، فنجد النتيجة حتى لو اختلفت ألفاظها.',
    definitionEn:
      'Searching by meaning rather than keywords: the query is embedded and the nearest vectors are returned.',
  },
  chunking: {
    id: 'chunking',
    en: 'Chunking',
    ar: 'تقسيم النصوص',
    preferred: 'Chunking',
    category: 'RAG',
    level: 'beginner',
    aliases: ['chunk', 'chunks', 'text splitting', 'splitter', 'التقطيع'],
    definitionAr:
      'تقسيم المستند إلى مقاطع صغيرة (chunks) قبل حساب الـ Embeddings، لأن حجم المقطع يحدد جودة الـ Retrieval بشكل مباشر.',
    definitionEn:
      'Splitting documents into smaller passages before embedding them; chunk size directly drives retrieval quality.',
  },
  retrieval: {
    id: 'retrieval',
    en: 'Retrieval',
    ar: 'الاسترجاع',
    preferred: 'Retrieval',
    category: 'RAG',
    level: 'beginner',
    aliases: ['retrieve'],
    definitionAr:
      'مرحلة جلب المقاطع الأكثر ارتباطاً بالـ query من مصدر خارجي قبل تمريرها للنموذج.',
    definitionEn:
      'The step that fetches the passages most relevant to a query from an external source before generation.',
  },
  retriever: {
    id: 'retriever',
    en: 'Retriever',
    ar: 'المُسترجِع',
    preferred: 'Retriever',
    category: 'RAG',
    level: 'intermediate',
    aliases: ['retrievers'],
    definitionAr: 'المكوّن المسؤول عن تنفيذ الـ Retrieval: يأخذ query ويُرجع قائمة documents مرتبة.',
    definitionEn: 'The component that performs retrieval: takes a query, returns ranked documents.',
  },
  retrieval_augmented_generation: {
    id: 'retrieval_augmented_generation',
    en: 'Retrieval-Augmented Generation',
    ar: 'التوليد المعزز بالاسترجاع',
    preferred: 'RAG',
    abbreviation: 'RAG',
    category: 'RAG',
    level: 'beginner',
    aliases: ['rag', 'retrieval augmented generation', 'التوليد المعزز'],
    definitionAr:
      'architecture يسمح للـ LLM بالوصول إلى external knowledge قبل توليد الإجابة: نبحث أولاً عن المقاطع المناسبة، ثم نمررها للنموذج داخل الـ context.',
    definitionEn:
      'An architecture that lets an LLM consult external knowledge before answering: retrieve relevant passages, then generate grounded in them.',
    exampleAr: 'مسار RAG المعتاد: Chunking ← Embeddings ← Vector Database ← Retrieval ← LLM.',
  },
  reranking: {
    id: 'reranking',
    en: 'Reranking',
    ar: 'إعادة الترتيب',
    preferred: 'Reranking',
    category: 'RAG',
    level: 'intermediate',
    aliases: ['rerank', 'reranker', 'cross-encoder', 'إعادة ترتيب'],
    definitionAr:
      'خطوة بعد الـ Retrieval يقيّم فيها نموذج أدق مدى ارتباط كل document بالـ query، فيعيد ترتيب النتائج ويضع الأكثر صلة في المقدمة.',
    definitionEn:
      'A post-retrieval step where a stronger model re-scores each document against the query and reorders the results.',
    exampleAr: 'الترتيب العملي: Retrieval ← Reranking ← LLM.',
  },
  hybrid_search: {
    id: 'hybrid_search',
    en: 'Hybrid Search',
    ar: 'البحث الهجين',
    preferred: 'Hybrid Search',
    category: 'RAG',
    level: 'advanced',
    aliases: ['bm25', 'keyword search', 'sparse retrieval', 'بحث هجين'],
    definitionAr:
      'دمج البحث الدلالي (vectors) مع البحث بالكلمات المفتاحية (BM25) لتغطية أفضل، خصوصاً مع الأسماء والأرقام والأكواد.',
    definitionEn:
      'Combining vector (semantic) search with keyword search (BM25) for better coverage, especially of names, numbers and code.',
  },
  query_expansion: {
    id: 'query_expansion',
    en: 'Query Expansion',
    ar: 'توسيع الاستعلام',
    preferred: 'Query Expansion',
    category: 'RAG',
    level: 'advanced',
    aliases: ['query rewriting', 'hyde'],
    definitionAr:
      'إعادة صياغة الـ query أو توليد صيغ إضافية له قبل الـ Retrieval لزيادة فرصة العثور على المقاطع الصحيحة.',
    definitionEn:
      'Rewriting or generating extra variants of a query before retrieval to raise the chance of hitting the right passages.',
  },
  knowledge_graph: {
    id: 'knowledge_graph',
    en: 'Knowledge Graph',
    ar: 'الرسم المعرفي',
    preferred: 'Knowledge Graph',
    category: 'RAG',
    level: 'advanced',
    aliases: ['graph rag', 'graphrag'],
    definitionAr:
      'تمثيل المعرفة كعُقد وعلاقات بدل نصوص مسطّحة، ويُستخدم مع الـ RAG للإجابة عن أسئلة تحتاج ربط عدة حقائق.',
    definitionEn:
      'Knowledge represented as entities and relations rather than flat text, used with RAG for multi-hop questions.',
  },
  grounding: {
    id: 'grounding',
    en: 'Grounding',
    ar: 'الإسناد إلى المصادر',
    preferred: 'Grounding',
    category: 'RAG',
    level: 'intermediate',
    aliases: ['citations', 'source attribution'],
    definitionAr:
      'إلزام النموذج بأن تكون إجابته مبنية على مقاطع مُسترجَعة فعلاً مع ذكر المصدر — الوسيلة العملية لتقليل الـ Hallucination.',
    definitionEn:
      'Constraining answers to retrieved evidence and citing it — the practical defence against hallucination.',
  },
  top_k: {
    id: 'top_k',
    en: 'Top-k',
    ar: 'أفضل k نتيجة',
    preferred: 'Top-k',
    category: 'RAG',
    level: 'beginner',
    aliases: ['top k', 'k results'],
    definitionAr:
      'عدد النتائج التي نطلبها من الـ Retriever. زيادته ترفع فرص التغطية لكنها تستهلك context أكثر.',
    definitionEn:
      'How many results to request from the retriever; larger k improves recall but spends more context.',
  },

  // ── Agents ────────────────────────────────────────────────────────────
  agent: {
    id: 'agent',
    en: 'AI Agent',
    ar: 'وكيل ذكاء اصطناعي',
    preferred: 'AI Agent',
    category: 'Agents',
    level: 'intermediate',
    aliases: ['agent', 'agents', 'agentic', 'الوكيل', 'الوكلاء'],
    definitionAr:
      'نظام يستخدم LLM ليقرر بنفسه الخطوة التالية ويستدعي tools لتنفيذها، ويكرّر ذلك في loop حتى يصل للهدف.',
    definitionEn:
      'A system where an LLM decides the next step, calls tools to execute it, and loops until the goal is met.',
  },
  tool_calling: {
    id: 'tool_calling',
    en: 'Tool Calling',
    ar: 'استدعاء الأدوات',
    preferred: 'Tool Calling',
    category: 'Agents',
    level: 'intermediate',
    aliases: ['tools', 'tool use', 'استدعاء أدوات'],
    definitionAr:
      'قدرة النموذج على طلب تنفيذ أداة خارجية (بحث، قاعدة بيانات، API) بدل محاولة الإجابة من ذاكرته.',
    definitionEn:
      'A model requesting execution of an external tool (search, database, API) instead of answering from memory.',
  },
  function_calling: {
    id: 'function_calling',
    en: 'Function Calling',
    ar: 'استدعاء الدوال',
    preferred: 'Function Calling',
    category: 'Agents',
    level: 'intermediate',
    aliases: ['function call'],
    definitionAr:
      'الشكل التقني للـ Tool Calling: تصف الدالة و parameters بـ schema، فيرد النموذج بـ JSON يحدد الدالة والوسائط.',
    definitionEn:
      'The concrete form of tool calling: you describe functions and parameters as a schema, the model replies with JSON naming the call.',
  },
  mcp: {
    id: 'mcp',
    en: 'Model Context Protocol',
    ar: 'بروتوكول سياق النموذج',
    preferred: 'MCP',
    abbreviation: 'MCP',
    category: 'Agents',
    level: 'advanced',
    aliases: ['mcp', 'model context protocol'],
    definitionAr:
      'بروتوكول مفتوح لتوصيل النماذج بمصادر البيانات والـ tools بواجهة موحّدة بدل كتابة تكامل مخصص لكل أداة.',
    definitionEn:
      'An open protocol for connecting models to data sources and tools through one standard interface.',
  },
  orchestration: {
    id: 'orchestration',
    en: 'Orchestration',
    ar: 'تنسيق المهام',
    preferred: 'Orchestration',
    category: 'Agents',
    level: 'advanced',
    aliases: ['workflow', 'orchestrator'],
    definitionAr:
      'إدارة تسلسل الخطوات بين النماذج والـ tools والشروط والأخطاء — وهو ما تقدّمه أدوات مثل LangGraph.',
    definitionEn:
      'Coordinating the sequence of models, tools, branching and failures — what frameworks like LangGraph provide.',
  },
  memory: {
    id: 'memory',
    en: 'Memory',
    ar: 'الذاكرة',
    preferred: 'Memory',
    category: 'Agents',
    level: 'intermediate',
    aliases: ['conversation memory', 'short-term memory', 'long-term memory'],
    definitionAr:
      'ما يحتفظ به النظام بين الرسائل أو الجلسات: تاريخ المحادثة، ملخصات، أو حقائق مخزّنة في Vector Database.',
    definitionEn:
      'What the system keeps between turns or sessions: chat history, summaries, or facts stored in a vector database.',
  },
  human_in_the_loop: {
    id: 'human_in_the_loop',
    en: 'Human-in-the-Loop',
    ar: 'تدخل بشري في المسار',
    preferred: 'Human-in-the-Loop',
    abbreviation: 'HITL',
    category: 'Agents',
    level: 'advanced',
    aliases: ['hitl', 'human in the loop', 'approval step'],
    definitionAr: 'إيقاف الـ AI Agent عند خطوة حساسة لانتظار موافقة إنسان قبل التنفيذ.',
    definitionEn: 'Pausing an agent at a sensitive step to wait for human approval before it acts.',
  },
  guardrails: {
    id: 'guardrails',
    en: 'Guardrails',
    ar: 'ضوابط الأمان',
    preferred: 'Guardrails',
    category: 'Agents',
    level: 'advanced',
    aliases: ['safety filters', 'content filtering'],
    definitionAr: 'قيود وفحوصات حول النموذج: تحقق من المدخلات والمخرجات، وحدود صلاحيات الـ tools.',
    definitionEn:
      'Checks and constraints around a model: input/output validation and limits on what tools may do.',
  },

  // ── Training & adaptation ─────────────────────────────────────────────
  fine_tuning: {
    id: 'fine_tuning',
    en: 'Fine-tuning',
    ar: 'الضبط الدقيق',
    preferred: 'Fine-tuning',
    category: 'Training',
    level: 'intermediate',
    aliases: ['finetuning', 'fine tuning', 'fine-tune'],
    definitionAr:
      'إكمال تدريب نموذج جاهز على بياناتك لتغيير أسلوبه أو تخصصه، ويُلجأ إليه حين لا يكفي الـ Prompt Engineering ولا الـ RAG.',
    definitionEn:
      "Continuing training of a pretrained model on your own data to change its style or specialism — used when prompting and RAG aren't enough.",
  },
  lora: {
    id: 'lora',
    en: 'Low-Rank Adaptation',
    ar: 'التكييف منخفض الرتبة',
    preferred: 'LoRA',
    abbreviation: 'LoRA',
    category: 'Training',
    level: 'advanced',
    aliases: ['lora', 'qlora', 'peft', 'parameter efficient fine-tuning'],
    definitionAr:
      'أسلوب Fine-tuning يدرّب مصفوفات إضافية صغيرة فقط بدل كل أوزان النموذج، فيوفّر ذاكرة GPU وتكلفة.',
    definitionEn:
      'A fine-tuning method that trains small adapter matrices instead of all weights, cutting GPU memory and cost.',
  },
  quantization: {
    id: 'quantization',
    en: 'Quantization',
    ar: 'تقليل الدقة العددية',
    preferred: 'Quantization',
    category: 'Training',
    level: 'advanced',
    aliases: ['quantized', 'int8', '4-bit', 'gguf'],
    definitionAr:
      'تقليل دقة أوزان النموذج (مثلاً من 16-bit إلى 4-bit) لتشغيله على أجهزة أصغر مقابل انخفاض بسيط في الجودة.',
    definitionEn:
      'Reducing the numeric precision of model weights (e.g. 16-bit to 4-bit) to run on smaller hardware at a small quality cost.',
  },
  pretraining: {
    id: 'pretraining',
    en: 'Pretraining',
    ar: 'التدريب المسبق',
    preferred: 'Pretraining',
    category: 'Training',
    level: 'advanced',
    aliases: ['pre-training', 'foundation model'],
    definitionAr: 'المرحلة الأولى والأغلى: تدريب النموذج من الصفر على كميات ضخمة من البيانات العامة.',
    definitionEn:
      'The first and most expensive stage: training a model from scratch on vast general-purpose data.',
  },
  rlhf: {
    id: 'rlhf',
    en: 'Reinforcement Learning from Human Feedback',
    ar: 'التعلم المعزز بالتغذية الراجعة البشرية',
    preferred: 'RLHF',
    abbreviation: 'RLHF',
    category: 'Training',
    level: 'advanced',
    aliases: ['rlhf', 'dpo', 'alignment'],
    definitionAr: 'مرحلة تدريب تستخدم تفضيلات بشرية لجعل إجابات النموذج أكثر فائدة وأماناً.',
    definitionEn:
      'A training stage that uses human preference data to make model responses more helpful and safe.',
  },
  overfitting: {
    id: 'overfitting',
    en: 'Overfitting',
    ar: 'الإفراط في التخصيص',
    preferred: 'Overfitting',
    category: 'Training',
    level: 'beginner',
    aliases: ['underfitting'],
    definitionAr:
      'أن يحفظ النموذج بيانات التدريب بدل أن يتعلم النمط، فيكون ممتازاً على الـ training set وضعيفاً على البيانات الجديدة.',
    definitionEn:
      'When a model memorises the training set instead of learning the pattern, performing well in training and poorly in production.',
  },
  hyperparameter: {
    id: 'hyperparameter',
    en: 'Hyperparameter',
    ar: 'مُعامل التدريب',
    preferred: 'Hyperparameter',
    category: 'Training',
    level: 'intermediate',
    aliases: ['hyperparameters', 'learning rate', 'batch size', 'epoch'],
    definitionAr:
      'إعداد تختاره أنت قبل التدريب (learning rate، batch size، epochs) ولا يتعلمه النموذج بنفسه.',
    definitionEn:
      'A setting you choose before training (learning rate, batch size, epochs) that the model does not learn itself.',
  },

  // ── Data ──────────────────────────────────────────────────────────────
  dataset: {
    id: 'dataset',
    en: 'Dataset',
    ar: 'مجموعة البيانات',
    preferred: 'Dataset',
    category: 'Data',
    level: 'beginner',
    aliases: ['datasets', 'training set', 'test set', 'مجموعة بيانات'],
    definitionAr: 'مجموعة الأمثلة المستخدمة للتدريب أو التقييم، وجودتها تحدد سقف جودة النموذج.',
    definitionEn:
      'The collection of examples used for training or evaluation; its quality caps the model’s quality.',
  },
  data_pipeline: {
    id: 'data_pipeline',
    en: 'Pipeline',
    ar: 'مسار المعالجة',
    preferred: 'Pipeline',
    category: 'Data',
    level: 'beginner',
    aliases: ['pipelines', 'خط المعالجة'],
    definitionAr:
      'سلسلة خطوات مترابطة تتحول فيها البيانات من مصدرها إلى النتيجة النهائية، كل خطوة تُغذّي التي بعدها.',
    definitionEn:
      'A chain of connected steps carrying data from source to final result, each feeding the next.',
    exampleAr:
      'RAG pipeline: تحميل documents ← Chunking ← Embeddings ← تخزين ← Retrieval ← generation.',
  },
  ground_truth: {
    id: 'ground_truth',
    en: 'Ground Truth',
    ar: 'المرجع الصحيح',
    preferred: 'Ground Truth',
    category: 'Data',
    level: 'intermediate',
    aliases: ['labels', 'labelled data', 'gold set'],
    definitionAr: 'الإجابة الصحيحة المعتمدة التي نقارن بها مخرجات النظام أثناء التقييم.',
    definitionEn:
      'The verified correct answer a system’s output is measured against during evaluation.',
  },

  // ── Evaluation ────────────────────────────────────────────────────────
  evaluation: {
    id: 'evaluation',
    en: 'Evaluation',
    ar: 'التقييم',
    preferred: 'Evaluation',
    abbreviation: 'Evals',
    category: 'Evaluation',
    level: 'intermediate',
    aliases: ['evals', 'eval'],
    definitionAr:
      'قياس جودة النظام بمقاييس ثابتة على مجموعة اختبار، بدل الاعتماد على الانطباع بعد تجربة يدوية.',
    definitionEn:
      'Measuring system quality with fixed metrics on a test set, instead of relying on impressions from manual spot checks.',
  },
  llm_as_judge: {
    id: 'llm_as_judge',
    en: 'LLM-as-a-Judge',
    ar: 'استخدام نموذج كمُحكّم',
    preferred: 'LLM-as-a-Judge',
    category: 'Evaluation',
    level: 'advanced',
    aliases: ['llm as judge', 'model grading'],
    definitionAr:
      'استخدام LLM قوي لتقييم مخرجات نظام آخر وفق rubric محدّد، وهو الأسلوب الشائع لتقييم الإجابات المفتوحة.',
    definitionEn:
      'Using a strong LLM to score another system’s outputs against an explicit rubric — the common approach for open-ended answers.',
  },
  benchmark: {
    id: 'benchmark',
    en: 'Benchmark',
    ar: 'اختبار مرجعي',
    preferred: 'Benchmark',
    category: 'Evaluation',
    level: 'intermediate',
    aliases: ['benchmarks', 'leaderboard'],
    definitionAr: 'مجموعة اختبار قياسية معروفة تُقارن بها النماذج على أساس موحّد.',
    definitionEn: 'A standard test suite used to compare models on common ground.',
  },
  retrieval_quality: {
    id: 'retrieval_quality',
    en: 'Retrieval Quality',
    ar: 'جودة الاسترجاع',
    preferred: 'Retrieval Quality',
    category: 'Evaluation',
    level: 'intermediate',
    aliases: ['recall@k', 'precision', 'recall', 'mrr', 'ndcg'],
    definitionAr:
      'قياس مدى نجاح الـ Retrieval في جلب المقاطع الصحيحة بمقاييس مثل recall@k و precision. أغلب مشاكل الـ RAG تبدأ هنا لا في الـ LLM.',
    definitionEn:
      'How well retrieval surfaces the right passages, measured with recall@k, precision and similar. Most RAG failures start here, not in the LLM.',
  },

  // ── Serving & engineering ─────────────────────────────────────────────
  inference: {
    id: 'inference',
    en: 'Inference',
    ar: 'الاستدلال',
    preferred: 'Inference',
    category: 'Serving',
    level: 'beginner',
    aliases: ['الاستنتاج'],
    definitionAr:
      'تشغيل نموذج مُدرَّب للحصول على تنبؤ أو إجابة — أي كل استدعاء في الإنتاج، مقابل مرحلة الـ training.',
    definitionEn:
      'Running a trained model to get a prediction — every production call, as opposed to training.',
  },
  latency: {
    id: 'latency',
    en: 'Latency',
    ar: 'زمن الاستجابة',
    preferred: 'Latency',
    category: 'Serving',
    level: 'beginner',
    aliases: ['ttft', 'response time'],
    definitionAr:
      'الزمن الذي يستغرقه النظام للرد على الطلب. في الـ LLMs يُقاس أيضاً بـ time-to-first-token.',
    definitionEn:
      'How long the system takes to answer a request; for LLMs also measured as time-to-first-token.',
  },
  throughput: {
    id: 'throughput',
    en: 'Throughput',
    ar: 'سعة المعالجة',
    preferred: 'Throughput',
    category: 'Serving',
    level: 'intermediate',
    aliases: ['requests per second', 'rps', 'batching'],
    definitionAr: 'عدد الطلبات أو الـ tokens التي يعالجها النظام في وحدة الزمن.',
    definitionEn: 'How many requests or tokens the system processes per unit of time.',
  },
  streaming: {
    id: 'streaming',
    en: 'Streaming',
    ar: 'البث التدريجي',
    preferred: 'Streaming',
    category: 'Serving',
    level: 'intermediate',
    aliases: ['stream', 'sse'],
    definitionAr:
      'إرسال الإجابة token بعد token فور توليدها بدل انتظار اكتمالها، فيشعر المستخدم باستجابة أسرع.',
    definitionEn:
      'Sending the answer token by token as it is generated instead of waiting for completion, so the app feels faster.',
  },
  observability: {
    id: 'observability',
    en: 'Observability',
    ar: 'إمكانية المراقبة',
    preferred: 'Observability',
    category: 'Serving',
    level: 'advanced',
    aliases: ['tracing', 'monitoring', 'logging'],
    definitionAr:
      'القدرة على رؤية ما حدث داخل النظام: traces لكل خطوة، وتكلفة، و Latency، ومعدل الأخطاء.',
    definitionEn:
      'Being able to see what happened inside the system: per-step traces, cost, latency and error rates.',
  },
  caching: {
    id: 'caching',
    en: 'Caching',
    ar: 'التخزين المؤقت',
    preferred: 'Caching',
    category: 'Serving',
    level: 'intermediate',
    aliases: ['cache', 'prompt caching', 'semantic cache'],
    definitionAr: 'حفظ نتائج الطلبات المتكررة لإعادة استخدامها، فيقل الـ Latency والتكلفة.',
    definitionEn: 'Storing results of repeated requests for reuse, cutting latency and cost.',
  },
  cost_per_token: {
    id: 'cost_per_token',
    en: 'Cost per Token',
    ar: 'تكلفة التوكن',
    preferred: 'Cost per Token',
    category: 'Serving',
    level: 'beginner',
    aliases: ['token cost', 'pricing'],
    definitionAr:
      'سعر الـ input والـ output tokens لدى مزوّد النموذج، وهو أساس حساب تكلفة أي feature.',
    definitionEn:
      'The provider’s price for input and output tokens — the basis of any feature’s unit economics.',
  },
  model_serving: {
    id: 'model_serving',
    en: 'Model Serving',
    ar: 'تشغيل النموذج كخدمة',
    preferred: 'Model Serving',
    category: 'Serving',
    level: 'advanced',
    aliases: ['serving', 'vllm', 'inference server'],
    definitionAr: 'تشغيل النموذج خلف API قابل للتوسّع مع إدارة الـ batching وذاكرة الـ GPU.',
    definitionEn: 'Running a model behind a scalable API, managing batching and GPU memory.',
  },
  api: {
    id: 'api',
    en: 'API',
    ar: 'واجهة برمجية',
    preferred: 'API',
    abbreviation: 'API',
    category: 'Engineering',
    level: 'beginner',
    aliases: ['apis', 'endpoint', 'rest api', 'واجهة برمجة التطبيقات'],
    definitionAr: 'واجهة متفق عليها تتيح لبرنامج استدعاء خدمات برنامج آخر.',
    definitionEn: 'A defined interface through which one program calls another’s services.',
  },
  backend: {
    id: 'backend',
    en: 'Backend',
    ar: 'الواجهة الخلفية',
    preferred: 'Backend',
    category: 'Engineering',
    level: 'beginner',
    aliases: ['server-side', 'الباك اند'],
    definitionAr: 'الجزء الذي يعمل على الخادم: المنطق وقواعد البيانات والـ APIs.',
    definitionEn: 'The server-side half of a system: logic, databases and APIs.',
  },
  frontend: {
    id: 'frontend',
    en: 'Frontend',
    ar: 'الواجهة الأمامية',
    preferred: 'Frontend',
    category: 'Engineering',
    level: 'beginner',
    aliases: ['client-side', 'الفرونت اند'],
    definitionAr: 'الجزء الذي يراه المستخدم ويتفاعل معه في المتصفح أو التطبيق.',
    definitionEn: 'The part users see and interact with in the browser or app.',
  },
  deployment: {
    id: 'deployment',
    en: 'Deployment',
    ar: 'النشر',
    preferred: 'Deployment',
    category: 'Engineering',
    level: 'beginner',
    aliases: ['deploy', 'ci/cd'],
    definitionAr: 'نقل الكود من بيئة التطوير إلى بيئة الإنتاج ليستخدمه المستخدمون فعلياً.',
    definitionEn: 'Moving code from development into production where real users reach it.',
  },
  containerization: {
    id: 'containerization',
    en: 'Containerization',
    ar: 'الحاويات',
    preferred: 'Containerization',
    category: 'Engineering',
    level: 'intermediate',
    aliases: ['container', 'containers', 'dockerize'],
    definitionAr:
      'تغليف التطبيق مع اعتمادياته في container يعمل بنفس الشكل على أي جهاز — عبر Docker غالباً.',
    definitionEn:
      'Packaging an application with its dependencies into a container that runs identically anywhere — usually with Docker.',
  },
  framework: {
    id: 'framework',
    en: 'Framework',
    ar: 'إطار عمل',
    preferred: 'Framework',
    category: 'Engineering',
    level: 'beginner',
    aliases: ['frameworks', 'إطار العمل'],
    definitionAr: 'مكتبة تفرض بنية جاهزة وتوفّر مكونات متكاملة بدل بنائها من الصفر.',
    definitionEn:
      'A library that supplies structure and ready components instead of building from scratch.',
  },
}

/** Stable array form — ordered by category, then English term. */
export const TERM_LIST: TechnicalTermEntry[] = Object.values(AI_TERMS).sort(
  (a, b) => a.category.localeCompare(b.category) || a.en.localeCompare(b.en)
)

export const TERM_CATEGORIES: TermCategory[] = [
  'LLM',
  'RAG',
  'Agents',
  'Training',
  'Data',
  'Evaluation',
  'Serving',
  'Engineering',
]
