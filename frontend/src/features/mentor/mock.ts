import type {
  HintLevel, InterviewReportV2, LearnerModel, MentorBlock, MentorContextRef, MentorIntent, MentorMessageV2,
  MentorSuggestion, PlanBlock, QuizAnswerResult, ReviewComment, ReviewResult, StudyPlanV2,
} from './types'

/**
 * The Mentor v2 server, stood in for until the backend has it (docs/backend-requests.md). It keeps
 * the rules the real one must keep, so the screens can be built and checked against them:
 *
 * - a quiz block never carries its answer; only `answerQuiz` knows it, and a wrong pick never
 *   reveals it;
 * - `HINT` level 4 is refused without `confirm: true`;
 * - a review reads the code and says so (`executed: false`);
 * - proactive messages and quick quizzes cost 0, an ordinary reply 2;
 * - one suggestion per 24 hours;
 * - skill confidence only moves on evidence the server saw.
 *
 * State is in memory plus localStorage for the thread, the approved plan and the suggestion
 * cooldown. Nothing here is a claim about the learner: it is a fixture.
 */

export const MESSAGE_CREDITS = 2
export const COOLDOWN_MS = 24 * 60 * 60 * 1000
const PLAN_KEY = 'masar:mentor-v2:plan'
const EXTRA_KEY = 'masar:mentor-v2:plan-extra'
const COOLDOWN_KEY = 'masar:mentor-v2:suggestion-until'
const PROACTIVE_KEY = 'masar:mentor-v2:proactive-until'

export type Lang = 'ar' | 'en'
const pick = (lang: Lang, ar: string, en: string) => (lang === 'ar' ? ar : en)

/** Test seams: a clock, and a switch that makes the next call fail like a provider outage. */
export const mockControl = { now: () => Date.now(), failNext: false, delayMs: process.env.NODE_ENV === 'test' ? 0 : 280 }

async function latency() {
  if (mockControl.delayMs > 0) await new Promise((r) => setTimeout(r, mockControl.delayMs))
}
function maybeFail() {
  if (mockControl.failNext) {
    mockControl.failNext = false
    // Shaped like the real server's answer to a provider outage: a 503, credits refunded.
    throw Object.assign(new Error('provider_unavailable'), {
      code: 'provider_unavailable',
      response: { status: 503, data: { detail: 'The mentor is unavailable right now. Your credits were refunded.' } },
    })
  }
}

function storage(): Storage | null {
  try { return typeof window !== 'undefined' ? window.localStorage : null } catch { return null }
}
function read<T>(key: string, fallback: T): T {
  try { const raw = storage()?.getItem(key); return raw ? (JSON.parse(raw) as T) : fallback } catch { return fallback }
}
function write(key: string, value: unknown) {
  try { storage()?.setItem(key, JSON.stringify(value)) } catch { /* private mode: the state is per-load */ }
}

/** Demo seam for the blocked-wallet state: `/mentor?credits=0`. It is deliberately a mock-only
 * query value and never gets sent to the backend or treated as a real wallet balance. */
export function mockCreditBalanceFromQuery(): number | null {
  if (typeof window === 'undefined') return null
  const raw = new URLSearchParams(window.location.search).get('credits')
  if (raw === null || raw.trim() === '') return null
  const value = Number(raw)
  return Number.isFinite(value) && value >= 0 ? Math.floor(value) : null
}

let counter = 0
const nextId = (prefix: string) => `${prefix}-${mockControl.now().toString(36)}-${(counter++).toString(36)}`

// ── Intent ────────────────────────────────────────────────────────────────────

const KEYWORDS: [MentorIntent, RegExp][] = [
  ['SIMPLIFY', /بسّط|بسط|مش فاهم|simplif|don't understand|dont understand/i],
  ['HINT', /تلميح|hint/i],
  ['QUIZ', /اختبرني|quiz/i],
  ['DEBUG', /خطأ|error|bug|traceback|لا يعمل|not working/i],
  ['WHY', /لماذا|ليه|why/i],
  ['PRACTICE', /تمرين|practice/i],
  ['EXPLAIN', /اشرح|explain/i],
]

/** An explicit intent from the UI always wins; otherwise a cheap keyword read, never an LLM call. */
export function detectIntent(text: string, explicit?: MentorIntent): MentorIntent {
  if (explicit) return explicit
  for (const [intent, pattern] of KEYWORDS) if (pattern.test(text)) return intent
  return 'GENERAL_QUESTION'
}

// ── Messages ──────────────────────────────────────────────────────────────────

const QUIZ = {
  id: 'quiz-checkpointer-1',
  correct: 'a',
}

function quizBlock(lang: Lang): Extract<MentorBlock, { kind: 'quiz' }> {
  return {
    kind: 'quiz',
    grounding: 'lesson',
    lang,
    quizId: QUIZ.id,
    question: pick(lang, 'ما الذي يجعل الوكيل يستأنف نفس المحادثة عند استدعاء جديد؟', 'What makes the agent resume the same conversation on a new call?'),
    options: [
      { id: 'a', text: pick(lang, 'تمرير thread_id ثابت داخل config', 'Passing a stable thread_id inside config') },
      { id: 'b', text: pick(lang, 'إنشاء graph جديد في كل استدعاء', 'Building a new graph on every call') },
      { id: 'c', text: pick(lang, 'رفع قيمة temperature', 'Raising the temperature') },
    ],
  }
}

function replyBlocks(intent: MentorIntent, ctx: MentorContextRef, text: string, lang: Lang): MentorBlock[] {
  const inLesson = !!ctx.lessonId
  const selected = ctx.selectedText?.trim()
  // What the lesson does not teach is labelled as extra, not passed off as the lesson.
  const extra = !!selected && /sqlite|postgres|saver/i.test(selected) && !/memorysaver/i.test(selected)
  const grounding = !inLesson ? 'general' : extra ? 'extra' : 'lesson'
  const sourceLessonId = extra ? '8' : inLesson ? ctx.lessonId : undefined
  const quote = selected ? `«${selected.slice(0, 80)}» ` : ''

  switch (intent) {
    case 'SIMPLIFY':
      return [
        { kind: 'text', grounding, sourceLessonId, text: pick(lang,
          `${quote}فكّر في الـ Checkpointer كأنه «حفظ اللعبة»: بعد كل خطوة يلتقط لقطة، وبنفس الاسم (thread_id) ترجع لنفس النقطة.`,
          `${quote}Think of the Checkpointer as a "save game": after every step it takes a snapshot, and with the same name (thread_id) you come back to the same point.`) },
        { kind: 'check', grounding, sourceLessonId, question: pick(lang, 'لو غيّرت thread_id بين استدعاءين، ماذا يتذكّر الوكيل؟', 'If you change thread_id between two calls, what does the agent remember?') },
      ]
    case 'SOCRATIC':
      return [{ kind: 'text', grounding, sourceLessonId, text: pick(lang,
        'قبل أن أجيب: لو استُدعي الـ graph مرتين بنفس الرسالة، ما الذي يميّز الاستدعاء الثاني عن الأول؟',
        'Before I answer: if the graph is called twice with the same message, what tells the second call apart from the first?') }]
    case 'QUIZ':
      return [quizBlock(lang)]
    case 'DEBUG':
      return [
        { kind: 'text', grounding, sourceLessonId, text: pick(lang,
          'لم أشغّل الكود، أقرؤه فقط. انظر إلى سطر compile: هل يصل الـ checkpointer إلى الـ graph؟',
          'I have not run your code, I only read it. Look at the compile line: does the checkpointer reach the graph?') },
        { kind: 'code', grounding, sourceLessonId, lang: 'python', code: 'graph = builder.compile(checkpointer=MemorySaver())' },
      ]
    case 'PRACTICE':
      return [{ kind: 'text', grounding, sourceLessonId, text: pick(lang,
        'تمرين صغير: اجعل الوكيل يتذكّر اسمك بين استدعاءين، ثم اختبره بـ thread_id مختلف.',
        'A small exercise: make the agent remember your name across two calls, then test it with a different thread_id.') }]
    case 'REVIEW':
      return [
        { kind: 'text', grounding, sourceLessonId, text: pick(lang, 'ملخّص الدرس في سلسلة واحدة:', 'The lesson in one chain:') },
        { kind: 'concept_chain', grounding, sourceLessonId, nodes: ['State', 'Checkpointer', 'thread_id', 'Resume', 'SqliteSaver'], focus: 1 },
      ]
    case 'CONNECT':
    case 'WHY':
      return [
        { kind: 'text', grounding, sourceLessonId, text: pick(lang,
          `${quote}بدون ذاكرة لا يستطيع الوكيل إكمال محادثة، وهذا ما يفتح الباب لما بعده في الدورة.`,
          `${quote}Without memory an agent cannot hold a conversation, which is what the rest of the course builds on.`) },
        { kind: 'concept_chain', grounding, sourceLessonId, nodes: ['State', 'Checkpointer', 'thread_id', 'Resume', 'SqliteSaver'], focus: 1 },
      ]
    case 'EXPLAIN':
      return [
        { kind: 'text', grounding, sourceLessonId, text: pick(lang,
          `${quote}الـ Checkpointer يحفظ حالة الـ graph بعد كل عقدة تحت مفتاح thread_id، فيكمل الاستدعاء التالي من آخر لقطة.`,
          `${quote}The Checkpointer saves the graph's state after every node under a thread_id key, so the next call resumes from the last snapshot.`) },
        { kind: 'concept_chain', grounding, sourceLessonId, nodes: ['State', 'Checkpointer', 'thread_id', 'Resume', 'SqliteSaver'], focus: 1 },
        { kind: 'check', grounding, sourceLessonId, question: pick(lang, 'بكلماتك: ما الذي يُحفظ بعد كل عقدة؟', 'In your own words: what is saved after every node?') },
      ]
    default:
      return [{ kind: 'text', grounding, sourceLessonId, text: inLesson
        ? pick(lang, `سؤالك عن «${text.slice(0, 60)}» — لنربطه بما في هذا الدرس.`, `Your question about "${text.slice(0, 60)}": let's tie it to this lesson.`)
        : pick(lang, `إجابة عامة، لم أربطها بدرس محدد: ${text.slice(0, 60)}`, `A general answer, not tied to a lesson: ${text.slice(0, 60)}`) }]
  }
}

export async function mockSendMessage(
  body: { text: string; intent?: MentorIntent; context: MentorContextRef },
  lang: Lang = 'ar',
): Promise<MentorMessageV2> {
  await latency()
  maybeFail()
  const intent = detectIntent(body.text, body.intent)
  return {
    id: nextId('m'),
    role: 'mentor',
    intent,
    blocks: replyBlocks(intent, body.context, body.text, lang),
    // Quick quizzes are free; everything else is one ordinary message.
    creditCost: intent === 'QUIZ' ? 0 : MESSAGE_CREDITS,
  }
}

// ── Hints ─────────────────────────────────────────────────────────────────────

export class HintConfirmRequired extends Error {
  constructor() { super('confirm_required') }
}

export async function mockHint(
  body: { exerciseId: string; level: HintLevel; confirm?: boolean },
  lang: Lang = 'ar',
): Promise<MentorMessageV2> {
  await latency()
  maybeFail()
  if (body.level === 4 && !body.confirm) throw new HintConfirmRequired()
  const labels: Record<HintLevel, string> = {
    1: pick(lang, 'تلميح مفاهيمي', 'Conceptual nudge'),
    2: pick(lang, 'اتجاه محدد', 'A specific direction'),
    3: pick(lang, 'إرشاد مفصّل', 'Detailed guidance'),
    4: pick(lang, 'الحل', 'The solution'),
  }
  const texts: Record<HintLevel, string> = {
    1: pick(lang, 'ما الذي يحدّد أي محادثة يكمل الوكيل منها؟ ابحث عن «المفتاح» الذي يربط الاستدعاءات.', 'What decides which conversation the agent resumes? Look for the key that links calls together.'),
    2: pick(lang, 'الـ graph يحتاج checkpointer عند compile، والاستدعاء يحتاج thread_id داخل config.', 'The graph needs a checkpointer at compile time, and the call needs a thread_id inside config.'),
    3: pick(lang, 'مرّر MemorySaver() إلى compile، ثم ضع thread_id في {"configurable": {...}} كوسيط ثانٍ لـ invoke.', 'Pass MemorySaver() to compile, then put thread_id in {"configurable": {...}} as the second argument of invoke.'),
    4: pick(lang, 'هذا هو الحل الكامل:', 'Here is the full solution:'),
  }
  const code = body.level === 4
    ? 'graph = builder.compile(checkpointer=MemorySaver())\n\ndef run(message: str, thread_id: str):\n    config = {"configurable": {"thread_id": thread_id}}\n    return graph.invoke({"messages": [message]}, config)\n'
    : undefined
  return {
    id: nextId('m'), role: 'mentor', intent: 'HINT', creditCost: MESSAGE_CREDITS,
    blocks: [{ kind: 'hint', grounding: 'lesson', level: body.level, label: labels[body.level], text: texts[body.level], code }],
  }
}

// ── Quiz ──────────────────────────────────────────────────────────────────────

// The server's view of what the learner knows; a correct answer is evidence, one miss is not a verdict.
const skillState = { checkpointers: 0.58 }

/** The question a quiz block shows, in `lang` (the same question - it costs nothing and records nothing). */
export async function mockQuiz(quizId: string, lang: Lang = 'ar'): Promise<Extract<MentorBlock, { kind: 'quiz' }>> {
  await latency()
  if (quizId !== QUIZ.id) throw new Error('quiz_not_found')
  return quizBlock(lang)
}

export async function mockAnswerQuiz(body: { quizId: string; optionId: string }, lang: Lang = 'ar'): Promise<QuizAnswerResult> {
  await latency()
  maybeFail()
  const known = body.quizId === QUIZ.id
  if (known && body.optionId === QUIZ.correct) {
    const from = Math.round(skillState.checkpointers * 100)
    skillState.checkpointers = Math.min(1, skillState.checkpointers + 0.08)
    return {
      correct: true,
      feedback: [{ kind: 'text', grounding: 'lesson', text: pick(lang, 'صحيح — thread_id الثابت هو ما يربط الاستدعاءات بنفس المحادثة.', 'Correct: a stable thread_id is what ties calls to the same conversation.') }],
      skillDelta: { skill: 'Checkpointers', from, to: Math.round(skillState.checkpointers * 100) },
    }
  }
  return {
    correct: false,
    // Never says which option was right: it asks a question that leads there.
    feedback: [
      { kind: 'text', grounding: 'lesson', text: pick(lang, 'قريب — لنفكّر معاً.', 'Close. Let us think it through together.') },
      { kind: 'text', grounding: 'lesson', text: pick(lang, 'لو استُدعي الـ graph مرتين، كيف «يعرف» أن الاستدعاء الثاني من نفس المحادثة؟', 'If the graph is called twice, how does it "know" the second call belongs to the same conversation?') },
      { kind: 'check', grounding: 'lesson', question: pick(lang, 'سؤال أصغر: ما الاسم الذي نمرّره في config ليحدّد المحادثة؟', 'A smaller question: which name do we pass in config to identify the conversation?') },
    ],
  }
}

// ── Review (a static read) ────────────────────────────────────────────────────

const reviewRounds = new Map<string, number>()

export async function mockReview(body: { exerciseId?: string; code?: string; lang: string }, lang: Lang = 'ar'): Promise<ReviewResult> {
  await latency()
  maybeFail()
  const code = body.code ?? ''
  const lines = code.split('\n')
  const comments: ReviewComment[] = []
  lines.forEach((line, i) => {
    const n = i + 1
    if (/import\s+MemorySaver/.test(line)) comments.push({ line: n, severity: 'ok', title: pick(lang, 'الاستيراد صحيح', 'Import is right'), text: pick(lang, 'MemorySaver من المسار الصحيح.', 'MemorySaver comes from the right module.') })
    if (/\.compile\(\s*\)/.test(line)) comments.push({ line: n, severity: 'issue', title: pick(lang, 'compile بدون checkpointer', 'compile without a checkpointer'), text: pick(lang, 'الـ graph يُبنى بلا ذاكرة، فكل استدعاء يبدأ من الصفر. مرّر checkpointer هنا.', 'The graph is built without memory, so every call starts from scratch. Pass a checkpointer here.') })
    if (/\.invoke\(\s*\{[^}]*\}\s*\)/.test(line)) comments.push({ line: n, severity: 'issue', title: pick(lang, 'thread_id لا يصل إلى invoke', 'thread_id never reaches invoke'), text: pick(lang, 'المعامل thread_id موجود في الدالة لكنه لا يدخل في config، فلن يُستأنف شيء.', 'thread_id is a parameter but never goes into config, so nothing can resume.') })
  })
  if (comments.length > 0 && !comments.some((c) => c.severity === 'issue')) {
    comments.push({ line: Math.max(1, lines.length), severity: 'suggestion', title: pick(lang, 'فكّر في الإنتاج', 'Think about production'), text: pick(lang, 'MemorySaver يضيع عند إعادة التشغيل؛ الدرس القادم يعرض SqliteSaver.', 'MemorySaver is lost on restart; the next lesson covers SqliteSaver.') })
  }
  const key = body.exerciseId ?? 'pasted'
  const round = (reviewRounds.get(key) ?? 0) + 1
  reviewRounds.set(key, round)
  const steps = [
    pick(lang, 'اقرأ سطر compile: هل يحمل checkpointer؟', 'Read the compile line: does it carry a checkpointer?'),
    pick(lang, 'تتبّع thread_id من معاملات الدالة حتى invoke.', 'Follow thread_id from the function parameters to invoke.'),
    pick(lang, 'أعد التشغيل بـ thread_id مختلف وقارن النتيجة.', 'Run again with a different thread_id and compare.'),
  ]
  // Each further look at the same code unlocks one more step, so the answer is never handed over at once.
  return {
    executed: false,
    comments,
    debugSteps: steps.map((text, i) => ({ text, unlocked: i < Math.min(steps.length, round) })),
  }
}

// ── Learner model, suggestion ─────────────────────────────────────────────────

export async function mockLearner(lang: Lang = 'ar'): Promise<LearnerModel> {
  await latency()
  const c = skillState.checkpointers
  return {
    position: { track: 'AI Engineer', course: 'LangGraph', lesson: 'Lesson 7' },
    skills: [
      { name: 'State graphs', status: 'mastered', confidence: 0.91, evidence: [pick(lang, '٣ اختبارات صحيحة متتالية', '3 quizzes passed in a row')] },
      { name: 'Checkpointers', status: c >= 0.85 ? 'mastered' : 'learning', confidence: Math.round(c * 100) / 100, evidence: [pick(lang, 'تمرين ٣ قيد التنفيذ · اختبار واحد صحيح', 'Exercise 3 in progress · one quiz correct')] },
      { name: 'Retrieval evaluation', status: 'needs_review', confidence: 0.42, evidence: [pick(lang, 'خطأ متكرر في ٣ أسئلة', 'Repeated misses on 3 questions')] },
    ],
  }
}

export async function mockSuggestion(lang: Lang = 'ar'): Promise<MentorSuggestion | null> {
  await latency()
  const until = read<number>(COOLDOWN_KEY, 0)
  if (mockControl.now() < until) return null
  return {
    id: 'sug-ragas-1',
    text: pick(lang, 'درجاتك في Retrieval evaluation أقل من المتوسط. مراجعة قصيرة (١٥ دقيقة) قبل الدرس ٨ ترفع جاهزيتك.', 'Your Retrieval evaluation scores are below average. A short review (15 minutes) before lesson 8 lifts your readiness.'),
    action: { label: pick(lang, 'ابدأ المراجعة', 'Start the review'), href: '/mentor?tab=chat' },
  }
}

/** Starting or dismissing both start the 24-hour quiet period, server-side. */
export async function mockResolveSuggestion(_id: string): Promise<void> {
  write(COOLDOWN_KEY, mockControl.now() + COOLDOWN_MS)
}

/** A proactive card the mentor opens a chat with: free, and at most one a day. */
export function mockProactive(lang: Lang = 'ar'): MentorMessageV2 | null {
  if (mockControl.now() < read<number>(PROACTIVE_KEY, 0)) return null
  write(PROACTIVE_KEY, mockControl.now() + COOLDOWN_MS)
  return {
    id: nextId('p'), role: 'mentor', intent: 'QUIZ', creditCost: 0,
    // The trigger's code, as the server sends it; the card words it in whichever language is active.
    proactive: { trigger: 'lesson_completed' },
    blocks: [quizBlock(lang)],
  }
}

// ── Plan ──────────────────────────────────────────────────────────────────────

const iso = (d: Date) => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`

export function mockExtraBlocks(): PlanBlock[] { return read<PlanBlock[]>(EXTRA_KEY, []) }

export async function mockAddToPlan(blocks: PlanBlock[]): Promise<void> {
  write(EXTRA_KEY, [...mockExtraBlocks(), ...blocks])
}

export async function mockPlan(body: { weekStart: string; variant?: number }, lang: Lang = 'ar'): Promise<StudyPlanV2> {
  await latency()
  maybeFail()
  const start = new Date(`${body.weekStart}T00:00:00`)
  const v = body.variant ?? 0
  const b = (type: PlanBlock['type'], title: string, minutes: number, refId: string): PlanBlock => ({ type, title, minutes, refId })
  const week: PlanBlock[][] = [
    [b('lesson', 'LangGraph · ' + pick(lang, 'الدرس ٨', 'Lesson 8'), 15, '/courses/langgraph-agent-memory/lessons/1008'), b('exercise', pick(lang, 'تمرين SqliteSaver', 'SqliteSaver exercise'), 25, '/courses/langgraph-agent-memory/lessons/1008')],
    [b('review', 'Retrieval evaluation', 20, '/mentor?tab=chat'), b('exercise', 'Ragas · ' + pick(lang, 'تمرين قصير', 'short exercise'), 15, '/challenges')],
    [b('lesson', 'LangGraph · ' + pick(lang, 'الدرس ٩', 'Lesson 9'), 18, '/courses/langgraph-agent-memory/lessons/1009')],
    [b('exercise', pick(lang, 'تمرين الإنسان في الحلقة', 'Human-in-the-loop exercise'), 30, '/courses/langgraph-agent-memory/lessons/1009'), b('review', pick(lang, 'مراجعة الدروس ٧-٩', 'Review lessons 7-9'), 15, '/mentor?tab=chat')],
    [b('interview', pick(lang, 'مقابلة تجريبية: RAG', 'Mock interview: RAG'), 30, '/mentor?tab=interview')],
    [b('lesson', 'RAG · ' + pick(lang, 'الوحدة التالية', 'next unit'), 22, '/courses/langgraph-agent-memory'), b('review', pick(lang, 'اختبار سريع', 'Quick quiz'), 10, '/mentor?tab=chat')],
    [],
  ]
  const order = v % 2 === 0 ? week : [...week.slice(1, 6), week[0], week[6]]
  const extra = mockExtraBlocks()
  const days = order.map((blocks, i) => {
    const d = new Date(start)
    d.setDate(start.getDate() + i)
    return { date: iso(d), blocks: i === 1 ? [...blocks, ...extra] : blocks }
  })
  const totalMinutes = days.reduce((sum, d) => sum + d.blocks.reduce((s, x) => s + x.minutes, 0), 0)
  return {
    goal: pick(lang, 'أنهِ وحدة الذاكرة في LangGraph وارفع Retrieval evaluation', 'Finish the LangGraph memory unit and lift Retrieval evaluation'),
    totalMinutes,
    days,
    reasons: [
      pick(lang, 'Retrieval evaluation يحتاج مراجعة: أخطأت فيه ثلاث مرات.', 'Retrieval evaluation needs review: three misses.'),
      pick(lang, 'الدرس ٨ يكمل ما بدأته في الدرس ٧ مباشرة.', 'Lesson 8 continues straight from lesson 7.'),
      pick(lang, 'مقابلة واحدة في الأسبوع تكفي لقياس التقدّم.', 'One interview a week is enough to measure progress.'),
    ],
  }
}

export async function mockApprovePlan(plan: StudyPlanV2): Promise<void> {
  write(PLAN_KEY, plan)
}

export function mockApprovedPlan(): StudyPlanV2 | null {
  return read<StudyPlanV2 | null>(PLAN_KEY, null)
}

// ── Interview report ──────────────────────────────────────────────────────────

export async function mockInterviewReport(_id: string, lang: Lang = 'ar'): Promise<InterviewReportV2> {
  await latency()
  return {
    role: 'RAG Engineer',
    date: '2026-10-03',
    duration: 28,
    score: 7.4,
    verdict: pick(lang, 'جاهز تقريباً', 'Nearly ready'),
    questions: [
      { text: pick(lang, 'لماذا نقسّم المستندات إلى chunks؟', 'Why do we split documents into chunks?'), score: 8.5, quote: pick(lang, 'لأن النموذج له سياق محدود والبحث أدق على أجزاء صغيرة', 'Because the model has a limited context and search is sharper on small parts'), note: pick(lang, 'إجابة دقيقة؛ أضف ذكر overlap.', 'Accurate; mention overlap too.') },
      { text: pick(lang, 'كيف تقيس جودة الـ retrieval؟', 'How do you measure retrieval quality?'), score: 5.5, quote: pick(lang, 'أجرّبه بنفسي وأرى إن كانت النتائج مناسبة', 'I try it myself and see whether the results look right'), note: pick(lang, 'ينقصك مقاييس مثل recall@k و MRR.', 'You are missing metrics such as recall@k and MRR.') },
      { text: pick(lang, 'متى تفضّل SqliteSaver على MemorySaver؟', 'When do you prefer SqliteSaver over MemorySaver?'), score: 8, quote: pick(lang, 'عندما أحتاج أن تبقى المحادثة بعد إعادة التشغيل', 'When a conversation has to survive a restart'), note: pick(lang, 'صحيح ومختصر.', 'Correct and concise.') },
    ],
    strengths: [pick(lang, 'فهم واضح للـ chunking', 'A clear grasp of chunking'), pick(lang, 'إجابات مختصرة ومباشرة', 'Short, direct answers')],
    gaps: [pick(lang, 'مقاييس تقييم الـ retrieval', 'Retrieval evaluation metrics'), pick(lang, 'ذكر أمثلة من مشاريع حقيقية', 'Examples from real projects')],
    recommended: [
      { code: 'COURSE-009', title: pick(lang, 'تقييم الـ Retrieval بـ Ragas', 'Evaluating retrieval with Ragas'), minutes: 20, href: '/courses/langgraph-agent-memory' },
      { code: 'COURSE-009', title: pick(lang, 'Chunking المتقدّم', 'Advanced chunking'), minutes: 15, href: '/courses/langgraph-agent-memory' },
    ],
  }
}

/** For tests: forget every fixture's state. */
export function resetMentorMock() {
  skillState.checkpointers = 0.58
  reviewRounds.clear()
  mockControl.failNext = false
  mockControl.now = () => Date.now()
  for (const k of [PLAN_KEY, EXTRA_KEY, COOLDOWN_KEY, PROACTIVE_KEY]) { try { storage()?.removeItem(k) } catch { /* nothing */ } }
}
