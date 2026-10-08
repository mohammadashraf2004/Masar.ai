import type { HomeOverview } from './types'

/** Stands in for the backend until it can supply readiness, milestones and exam eligibility. */
export const MOCK_HOME_OVERVIEW: HomeOverview = {
  continueLearning: {
    courseTitle: 'LangGraph',
    lessonNumber: 7,
    lessonTotal: 12,
    lessonTitle: {
      en: 'Checkpointers and persisting conversation memory',
      ar: 'Checkpointers وحفظ ذاكرة المحادثة',
    },
    minutesLeft: 18,
    percent: 62,
    lessonHref: '/courses/langgraph-agent-memory/lessons/7',
    planHref: '/courses/langgraph-agent-memory',
  },
  readiness: {
    score: 72,
    weeklyDelta: 6,
    skills: [
      { name: { en: 'Retrieval & RAG', ar: 'Retrieval و RAG' }, value: 80 },
      { name: { en: 'Agents', ar: 'Agents' }, value: 64 },
      { name: { en: 'Deployment & Serving', ar: 'النشر و Serving' }, value: 58 },
      { name: { en: 'Evaluation', ar: 'Evaluation' }, value: 49 },
    ],
  },
  track: {
    title: { en: 'AI Engineer', ar: 'مهندس ذكاء اصطناعي' },
    en: 'AI Engineer',
    milestones: [
      { title: { en: 'Python for AI', ar: 'Python للذكاء الاصطناعي' }, meta: { en: '6 courses · 32 hours', ar: '٦ دورات · ٣٢ ساعة' }, status: 'done' },
      { title: { en: 'LLM fundamentals and prompting', ar: 'أساسيات LLM و Prompting' }, meta: { en: '4 courses · 20 hours', ar: '٤ دورات · ٢٠ ساعة' }, status: 'done' },
      { title: { en: 'RAG and vector databases', ar: 'RAG و Vector Databases' }, meta: { en: 'Qdrant · LlamaIndex · Ragas', ar: 'Qdrant · LlamaIndex · Ragas' }, status: 'now', percent: 64 },
      { title: { en: 'Agents with LangGraph', ar: 'Agents مع LangGraph' }, meta: { en: '3 courses · 26 hours', ar: '٣ دورات · ٢٦ ساعة' }, status: 'lock' },
      { title: { en: 'Deployment and evaluation', ar: 'النشر و Evaluation' }, meta: { en: 'FastAPI · vLLM · LangSmith', ar: 'FastAPI · vLLM · LangSmith' }, status: 'lock' },
    ],
  },
  exam: {
    title: 'RAG Engineer — Associate',
    minutes: 90,
    pointsAway: 3,
    requirements: [
      { label: { en: 'Finish the RAG unit', ar: 'إكمال وحدة RAG' }, done: true },
      { label: { en: 'Readiness score of 75 or more', ar: 'مؤشر جاهزية ٧٥ أو أكثر' }, done: false, value: '72/75' },
    ],
  },
  stats: { streakDays: 12, gradedExercises: 86 },
  mentor: {
    tip: {
      en: 'Your retrieval-evaluation scores are below your cohort average. Try the short Ragas exercise (15 minutes) before lesson 8 — it will lift your readiness score right away.',
      ar: 'درجاتك في Retrieval evaluation أقل من متوسط دفعتك. جرّب تمرين Ragas القصير (١٥ دقيقة) قبل الانتقال للدرس ٨ — سيرفع مؤشر جاهزيتك مباشرة.',
    },
    href: '/mentor',
  },
}
