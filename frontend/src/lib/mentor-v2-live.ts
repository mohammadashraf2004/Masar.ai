/**
 * Mentor v2: wire types for the live endpoints, and the per-endpoint
 * live flag.
 *
 * NEXT_PUBLIC_MENTOR_V2_LIVE is a comma-separated list of endpoints that
 * talk to the real API, e.g. `message,quiz`. Anything not listed stays on
 * the mock, so later endpoints (review, plan, interview report) can go
 * live one at a time without touching the ones already shipped.
 *
 * Read directly off `process.env.NEXT_PUBLIC_…` (not destructured) so Next
 * inlines it at build time.
 */

export type MentorV2Endpoint = 'message' | 'quiz' | 'review' | 'plan' | 'report'

const LIVE = new Set(
  (process.env.NEXT_PUBLIC_MENTOR_V2_LIVE ?? '')
    .split(',')
    .map(s => s.trim().toLowerCase())
    .filter(Boolean)
)

export function isMentorV2Live(endpoint: MentorV2Endpoint): boolean {
  return LIVE.has(endpoint)
}

// ─── Wire types (mirror backend/app/views/mentor_v2.py) ─────────────────

export type MentorV2Intent =
  | 'explain' | 'simplify' | 'example' | 'why' | 'hint'
  | 'socratic' | 'quiz' | 'practice' | 'review'

/** Where a block's content came from, in retrieval order. `general` means
 *  nothing in the course backs it (the "extra concept" pill). */
export type MentorV2Grounding = 'lesson' | 'module' | 'prerequisite' | 'mistakes' | 'general'

export interface MentorV2QuizQuestion {
  quizId: number
  questionIndex: number
  question: string
  /** No correct index: the server grades. */
  options: string[]
}

export interface MentorV2Block {
  kind: 'text' | 'code' | 'flow' | 'check' | 'hint' | 'quiz'
  grounding: MentorV2Grounding
  text?: string | null
  code?: string | null
  language?: string | null
  steps?: string[] | null
  level?: number | null
  source?: { lessonId: number; title: string } | null
  quiz?: MentorV2QuizQuestion | null
}

/** Only ids and the learner's words. Progress, mastery and grades are
 *  never sent: the server reads them itself and ignores any it is given. */
export interface MentorV2MessageRequest {
  content?: string
  lessonId?: number
  exerciseId?: number
  sessionId?: number
  intent?: MentorV2Intent
  selection?: string
  trigger?: 'lesson_completed'
  language?: 'ar' | 'en'
  terminologyMode?: 'arabic_first' | 'industry' | 'english_technical'
}

export interface MentorV2Reply {
  sessionId: number
  intent: MentorV2Intent
  intentSource: 'explicit' | 'rules' | 'model' | 'default' | 'trigger'
  proactive: boolean
  blocks: MentorV2Block[]
  creditsCharged: number
  fallback: boolean
  context: {
    lessonId: number | null
    lessonTitle: string | null
    moduleTitle: string | null
    exerciseId: number | null
    exerciseTitle: string | null
  }
}

export interface MentorV2QuizAnswerRequest {
  quizId: number
  questionIndex: number
  choice: number
  lessonId?: number
  language?: 'ar' | 'en'
}

export interface MentorV2SkillDelta {
  skill: string
  before: number
  after: number
  status: 'learning' | 'mastered' | 'needs_review'
  previousStatus: 'learning' | 'mastered' | 'needs_review'
}

export interface MentorV2QuizAnswer {
  correct: boolean
  feedback: MentorV2Block[]
  /** Present only when the skill's confidence actually changed. */
  skillDelta: MentorV2SkillDelta | null
}
