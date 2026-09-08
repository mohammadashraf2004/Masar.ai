/**
 * Job-oriented terminology mapping.
 *
 * The point of keeping terminology in English is employability, so the
 * platform has to close the loop and show *where* a term shows up: which
 * roles ask for it, and how it is phrased in a real job description.
 *
 * `terms` holds ids from AI_TERMS. Framework names live in `tools` — they
 * are proper nouns, not dictionary entries (see tech-names.ts).
 */
import { AI_TERMS, type TechnicalTermEntry } from './ai-terms'

export interface JobRole {
  id: string
  title: string
  /** Arabic one-liner: what this role actually does day to day. */
  summaryAr: string
  /** AI_TERMS ids this role's job descriptions lean on. */
  terms: string[]
  tools: string[]
  /** Verbatim-style phrasing a student will meet in a real posting. */
  jdPhrases: string[]
}

export const JOB_ROLES: JobRole[] = [
  {
    id: 'ai_engineer',
    title: 'AI Engineer',
    summaryAr: 'يبني تطبيقات فوق الـ LLMs: RAG، وAgents، وتكامل مع الأنظمة القائمة.',
    terms: [
      'large_language_model',
      'retrieval_augmented_generation',
      'embeddings',
      'vector_database',
      'prompt_engineering',
      'tool_calling',
      'evaluation',
      'latency',
    ],
    tools: ['Python', 'LangChain', 'FastAPI', 'Docker', 'Qdrant'],
    jdPhrases: [
      'Experience building RAG pipelines over internal knowledge bases',
      'Familiarity with vector databases and embedding models',
      'Ability to evaluate and improve retrieval quality',
    ],
  },
  {
    id: 'genai_engineer',
    title: 'Generative AI Engineer',
    summaryAr: 'يركّز على توليد المحتوى والمنتجات التوليدية، من الـ prompting حتى الإنتاج.',
    terms: [
      'prompt_engineering',
      'structured_output',
      'hallucination',
      'guardrails',
      'streaming',
      'cost_per_token',
      'evaluation',
    ],
    tools: ['OpenAI', 'Anthropic', 'Hugging Face', 'LangChain', 'Next.js'],
    jdPhrases: [
      'Hands-on prompt engineering and structured output design',
      'Experience shipping streaming LLM features to production',
      'Understanding of token cost and latency trade-offs',
    ],
  },
  {
    id: 'llm_engineer',
    title: 'LLM Engineer',
    summaryAr: 'يتعامل مع النماذج نفسها: fine-tuning، وتقييم، وتشغيلها بكفاءة.',
    terms: [
      'fine_tuning',
      'lora',
      'quantization',
      'inference',
      'model_serving',
      'benchmark',
      'throughput',
    ],
    tools: ['PyTorch', 'Hugging Face', 'vLLM', 'Docker', 'AWS'],
    jdPhrases: [
      'Fine-tuning open-weight models with LoRA/QLoRA',
      'Optimising inference throughput and GPU utilisation',
      'Benchmarking model quality against task-specific evals',
    ],
  },
  {
    id: 'rag_engineer',
    title: 'RAG Engineer',
    summaryAr: 'متخصص في أنظمة الاسترجاع: الـ chunking والـ retrieval والـ reranking وجودتها.',
    terms: [
      'chunking',
      'retrieval',
      'reranking',
      'hybrid_search',
      'query_expansion',
      'retrieval_quality',
      'grounding',
    ],
    tools: ['LlamaIndex', 'LangChain', 'Qdrant', 'pgvector', 'PostgreSQL'],
    jdPhrases: [
      'Designing chunking and indexing strategies for large document sets',
      'Improving recall@k with hybrid search and reranking',
      'Building grounded answers with source citations',
    ],
  },
  {
    id: 'ai_platform_engineer',
    title: 'AI Platform Engineer',
    summaryAr: 'يبني البنية التي تعمل عليها فرق الـ AI: خدمات، ومراقبة، وتكلفة، ونشر.',
    terms: [
      'deployment',
      'containerization',
      'observability',
      'caching',
      'throughput',
      'api',
      'orchestration',
    ],
    tools: ['Docker', 'Kubernetes', 'Terraform', 'PostgreSQL', 'Redis'],
    jdPhrases: [
      'Operating LLM services with tracing, cost and latency dashboards',
      'Containerised deployments on Kubernetes',
      'Designing internal APIs for AI product teams',
    ],
  },
  {
    id: 'ml_engineer',
    title: 'Machine Learning Engineer',
    summaryAr: 'يدرّب النماذج ويشغّلها في الإنتاج، من الـ dataset حتى الـ monitoring.',
    terms: [
      'dataset',
      'hyperparameter',
      'overfitting',
      'evaluation',
      'inference',
      'data_pipeline',
      'ground_truth',
    ],
    tools: ['Python', 'PyTorch', 'scikit-learn', 'MLflow', 'Airflow'],
    jdPhrases: [
      'End-to-end ownership of training pipelines',
      'Model evaluation against a held-out ground truth set',
      'Monitoring model performance after deployment',
    ],
  },
]

/** Roles whose job descriptions use a given term. */
export function rolesForTerm(termId: string): JobRole[] {
  return JOB_ROLES.filter((role) => role.terms.includes(termId))
}

/** Resolve a role's term ids to dictionary entries, skipping unknown ids. */
export function termsForRole(role: JobRole): TechnicalTermEntry[] {
  return role.terms.map((id) => AI_TERMS[id]).filter(Boolean)
}

/**
 * Roles relevant to a set of terms a course teaches, most-matching first.
 * Used by the "Where you'll see this" panel on a course page.
 */
export function rolesForTerms(termIds: string[]): Array<{ role: JobRole; matched: string[] }> {
  const wanted = new Set(termIds)
  return JOB_ROLES.map((role) => ({
    role,
    matched: role.terms.filter((id) => wanted.has(id)),
  }))
    .filter((entry) => entry.matched.length > 0)
    .sort((a, b) => b.matched.length - a.matched.length)
}
