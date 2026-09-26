import type { StringKey } from '@/lib/i18n'
import type { InterviewQuestion } from '@/types'

export type InterviewType = 'technical' | 'system_design' | 'behavioral'
export type InterviewLanguage = 'ar' | 'en'

export const INTERVIEW_TYPES: readonly InterviewType[] = ['technical', 'system_design', 'behavioral']
export const DURATIONS = [15, 30, 45] as const
export type Duration = (typeof DURATIONS)[number]

/** How many questions fit each length: the design's 30-minute interview has five. */
export const QUESTIONS_FOR: Record<Duration, number> = { 15: 3, 30: 5, 45: 8 }

/** What the backend charges for each question it generates (`mock_interview` in wallet_service). */
export const MOCK_INTERVIEW_CREDITS = 3

/** An answer that scores below this, on average, is one to practise again. Out of 10. */
export const WEAK_BELOW = 6

export type ScoreNote = { key: StringKey } | { text: string }

/** Out of 10 on each of the three things the design scores. */
export interface AnswerScore {
  accuracy: number
  structure: number
  clarity: number
  note: ScoreNote
}

export const SCORE_DIMENSIONS = ['accuracy', 'structure', 'clarity'] as const
export type ScoreDimension = (typeof SCORE_DIMENSIONS)[number]

export interface QuestionRecord {
  id: string
  text: string
  qtype: InterviewQuestion['question_type']
  hints: string[]
  /** Null until the learner has answered or skipped. */
  answer: string | null
  skipped: boolean
  score: AnswerScore | null
}

export interface InterviewSession {
  id: string
  role: string
  type: InterviewType
  language: InterviewLanguage
  durationMin: Duration
  totalQuestions: number
  startedAt: string
  endedAt: string | null
  questions: QuestionRecord[]
  /** The questions were carried over from an earlier interview (a retry), not generated. */
  retryOf: string | null
}

export function newQuestion(question: InterviewQuestion): QuestionRecord {
  return {
    id: `q-${Math.random().toString(36).slice(2, 10)}`,
    text: question.question,
    qtype: question.question_type,
    hints: question.hints ?? [],
    answer: null,
    skipped: false,
    score: null,
  }
}

export function scoreAverage(score: AnswerScore): number {
  return (score.accuracy + score.structure + score.clarity) / 3
}

const round1 = (n: number) => Math.round(n * 10) / 10

/** The mean of every scored answer's average, or null when nothing was scored. */
export function overallScore(session: InterviewSession): number | null {
  const scored = session.questions.filter((q) => q.score)
  if (scored.length === 0) return null
  return round1(scored.reduce((sum, q) => sum + scoreAverage(q.score!), 0) / scored.length)
}

/** The mean of one dimension over the scored answers, or null when nothing was scored. */
export function dimensionAverage(session: InterviewSession, dimension: ScoreDimension): number | null {
  const scored = session.questions.filter((q) => q.score)
  if (scored.length === 0) return null
  return round1(scored.reduce((sum, q) => sum + q.score![dimension], 0) / scored.length)
}

export function answeredCount(session: InterviewSession): number {
  return session.questions.filter((q) => q.answer !== null && !q.skipped).length
}

/** Skipped, or answered and scored under the bar. An answer nobody scored is not called weak. */
export function isWeak(question: QuestionRecord): boolean {
  if (question.skipped) return true
  return question.score !== null && scoreAverage(question.score) < WEAK_BELOW
}

export function weakQuestions(session: InterviewSession): QuestionRecord[] {
  return session.questions.filter(isWeak)
}

/** The last question that was answered and scored: what the side panel shows. */
export function lastScored(session: InterviewSession): QuestionRecord | null {
  for (let i = session.questions.length - 1; i >= 0; i--) {
    if (session.questions[i].score) return session.questions[i]
  }
  return null
}

/** Which of the generator's topics an interview type asks for. The API takes a free-text topic. */
export function topicFor(role: string, type: InterviewType): string {
  if (type === 'system_design') return `${role} system design`
  if (type === 'behavioral') return `Behavioral questions for a ${role}`
  return `${role} technical concepts`
}

/** The API's difficulty is the account's own level. */
export function difficultyFor(level: string | undefined): string {
  return level === 'beginner' || level === 'advanced' ? level : 'intermediate'
}

export function isFinished(session: InterviewSession): boolean {
  return session.endedAt !== null
}

export interface NewSessionInput {
  role: string
  type: InterviewType
  language: InterviewLanguage
  durationMin: Duration
  /** Questions to ask again (a retry). Without them the interview generates its own. */
  questions?: QuestionRecord[]
  retryOf?: string | null
}

/** A fresh interview, not yet saved. A retry asks exactly the questions it was given. */
export function buildSession(id: string, input: NewSessionInput, now: Date = new Date()): InterviewSession {
  const carried = input.questions ?? []
  return {
    id,
    role: input.role,
    type: input.type,
    language: input.language,
    durationMin: input.durationMin,
    totalQuestions: carried.length > 0 ? carried.length : QUESTIONS_FOR[input.durationMin],
    startedAt: now.toISOString(),
    endedAt: null,
    questions: carried,
    retryOf: input.retryOf ?? null,
  }
}

/** A question asked again: the same text, with the earlier answer and score cleared. */
export function freshCopy(question: QuestionRecord): QuestionRecord {
  return { ...question, id: `q-${Math.random().toString(36).slice(2, 10)}`, answer: null, skipped: false, score: null }
}

/** Ends an interview (a no-op if it has already ended). */
export function endSession(session: InterviewSession, now: Date = new Date()): InterviewSession {
  return session.endedAt ? session : { ...session, endedAt: now.toISOString() }
}
