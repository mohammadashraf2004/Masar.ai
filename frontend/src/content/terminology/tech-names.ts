/**
 * Official technology, framework and product names.
 *
 * These are never translated, transliterated or inflected — not in lesson
 * prose, not in the UI, not by the AI tutor. They are proper nouns, and a
 * student searching for "PyTorch" must find "PyTorch".
 *
 * Used by the content linter (backend/app/services/content/terminology_lint.py,
 * via the generated JSON) and by the authoring guidelines.
 */
export const TECH_NAMES: string[] = [
  // Languages & runtimes
  'Python',
  'TypeScript',
  'JavaScript',
  'SQL',
  'Node.js',
  // ML / DL
  'PyTorch',
  'TensorFlow',
  'JAX',
  'Keras',
  'scikit-learn',
  'NumPy',
  'pandas',
  'Hugging Face',
  'Transformers',
  'Diffusers',
  // LLM app layer
  'LangChain',
  'LangGraph',
  'LangSmith',
  'LlamaIndex',
  'Haystack',
  'DSPy',
  'Ollama',
  'vLLM',
  // Vector stores
  'FAISS',
  'Chroma',
  'Qdrant',
  'Pinecone',
  'Weaviate',
  'Milvus',
  'pgvector',
  // Providers & models
  'OpenAI',
  'Anthropic',
  'Claude',
  'GPT',
  'Gemini',
  'Llama',
  'Mistral',
  'Cohere',
  // Backend & infra
  'FastAPI',
  'Flask',
  'Django',
  'Docker',
  'Kubernetes',
  'PostgreSQL',
  'Redis',
  'MongoDB',
  'Kafka',
  'Airflow',
  'MLflow',
  'Terraform',
  'Git',
  'GitHub',
  'AWS',
  'GCP',
  'Azure',
  // Frontend
  'React',
  'Next.js',
  'Tailwind CSS',
]

/** Lowercased set for fast membership checks. */
export const TECH_NAME_SET: Set<string> = new Set(TECH_NAMES.map((n) => n.toLowerCase()))
