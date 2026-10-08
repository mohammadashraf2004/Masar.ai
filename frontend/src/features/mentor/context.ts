import type { MentorContextRef, MentorContextSelection } from './types'

/**
 * Empty until the authenticated server resolves the learner's last active or
 * explicitly selected lesson. A demo fixture must never become request data.
 *
 * Only ids go to the server. The labels below are for the chips, and are never sent.
 */
export const DEFAULT_CONTEXT: MentorContextSelection = {}

export function contextLabels(base: MentorContextSelection, language: 'ar' | 'en', n: (value: number) => string): { lesson: string | null; code: string | null } {
  const lesson = base.lessonId
    ? [base.courseTitle, base.lessonNumber ? (language === 'ar' ? `الدرس ${n(base.lessonNumber)}` : `Lesson ${base.lessonNumber}`) : null, base.lessonTitle]
        .filter(Boolean).join(' · ')
    : null
  const code = base.exerciseId ? (base.exerciseTitle || (language === 'ar' ? 'تمرين الكود' : 'Code exercise')) : null
  return { lesson, code }
}

/**
 * The `context` of one request, from the chips that are on: removing a chip removes its ids from
 * the request, so with both removed the mentor has nothing to ground an answer in and says so.
 */
export function buildContext(base: MentorContextRef, on: { lesson: boolean; code: boolean }, selectedText?: string): MentorContextRef {
  const context: MentorContextRef = {}
  if (on.lesson) {
    if (base.courseId) context.courseId = base.courseId
    if (base.lessonId) context.lessonId = base.lessonId
  }
  if (on.code && base.exerciseId) {
    context.exerciseId = base.exerciseId
    context.attachCode = true
  }
  if (selectedText) context.selectedText = selectedText
  return context
}
