/**
 * The Mentor v2 contract (Masar Mentor v2 brief, section 1). The server is the source of truth for
 * progress, mastery, grades, credits and quiz answers: the client sends ids, an intent, selected
 * text and what the learner typed, and shows what comes back. A quiz block never carries its answer.
 */

export type MentorIntent =
  | 'EXPLAIN' | 'SIMPLIFY' | 'HINT' | 'SOCRATIC' | 'DEBUG' | 'QUIZ' | 'PRACTICE'
  | 'REVIEW' | 'CONNECT' | 'WHY' | 'PROJECT_COACH' | 'CAREER_CONTEXT' | 'GENERAL_QUESTION'

export interface MentorContextRef {
  courseId?: string
  lessonId?: string
  exerciseId?: string
  attachCode?: boolean
  selectedText?: string
  /** What is in the exercise editor now - the learner's own draft, sent only with the code chip on. */
  code?: string
}

export interface MentorContextSelection extends MentorContextRef {
  courseTitle?: string
  lessonTitle?: string
  exerciseTitle?: string
  lessonNumber?: number
  lessonTotal?: number
}

export type Grounding = 'lesson' | 'extra' | 'general'
export type HintLevel = 1 | 2 | 3 | 4

/** `sourceCourseId` / `sourceTitle` are set by the server from the verified source, never by the model. */
type Grounded = { grounding: Grounding; sourceLessonId?: string; sourceCourseId?: string; sourceTitle?: string }

export type MentorBlock = Grounded & (
  | { kind: 'text'; text: string }
  | { kind: 'concept_chain'; nodes: string[]; focus: number }
  | { kind: 'code'; code: string; lang: string }
  | { kind: 'hint'; level: HintLevel; label: string; text: string; code?: string }
  // `lang` is the language the question and options are really written in. When the UI language
  // differs from it, the block asks for the same question again in the UI language.
  | { kind: 'quiz'; quizId: string; question: string; options: { id: string; text: string }[]; lang?: 'ar' | 'en' }
  | { kind: 'check'; question: string }
)

export interface MentorMessageV2 {
  id: string
  role: 'learner' | 'mentor'
  intent?: MentorIntent
  proactive?: { trigger: string }
  blocks: MentorBlock[]
  creditCost: number
  /** The stored answer to a send the server had already answered (a retry): not charged again. */
  replayed?: boolean
}

export interface SkillDelta { skill: string; from: number; to: number; status?: SkillStatus }

export interface QuizAnswerResult {
  correct: boolean
  feedback: MentorBlock[]
  skillDelta?: SkillDelta
}

export type ReviewSeverity = 'ok' | 'suggestion' | 'issue'

export interface ReviewComment { line: number; severity: ReviewSeverity; title: string; text: string }

export interface ReviewResult {
  /** Always false: a review reads the code, it never runs it. */
  executed: false
  /** The reviewer's overall assessment, when the server gave one. */
  summary?: string
  comments: ReviewComment[]
  debugSteps: { text: string; unlocked: boolean }[]
}

export type SkillStatus = 'mastered' | 'learning' | 'needs_review'

export interface LearnerModel {
  position: { track: string; course: string; lesson: string; courseId?: string | null; lessonId?: string | null }
  skills: { name: string; status: SkillStatus; confidence: number; evidence: string[] }[]
}

export interface MentorSuggestion { id: string; text: string; action: { label: string; href: string } }

export type PlanBlockType = 'lesson' | 'exercise' | 'review' | 'interview'
/** `refId` is an id (`lesson:12`, `mentor:chat`), or a path in the design fixtures; links are built
 * from `courseId`/`lessonId` by `planBlockHref`, never taken from server text. */
export interface PlanBlock {
  type: PlanBlockType; title: string; minutes: number; refId: string
  courseId?: string; lessonId?: string
  /** This block carries on a lesson started on an earlier day. */
  continues?: boolean
}
export interface PlanDay { date: string; blocks: PlanBlock[] }
export type StudyPlanStatus = 'ok' | 'no_enrollment' | 'all_done' | 'locked'
export interface StudyPlanV2 { goal: string; totalMinutes: number; days: PlanDay[]; reasons: string[]; status?: StudyPlanStatus }

export interface InterviewReportV2 {
  role: string
  date: string
  duration: number
  score: number
  verdict: string
  questions: { text: string; score: number; quote: string; note: string }[]
  strengths: string[]
  gaps: string[]
  recommended: { code: string; title: string; minutes: number; href: string }[]
}
