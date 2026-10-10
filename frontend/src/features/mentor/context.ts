import type { MentorContextRef, MentorContextSelection } from './types'

/**
 * Empty until the authenticated server resolves the learner's last active or
 * explicitly selected lesson. A demo fixture must never become request data.
 *
 * Only ids go to the server. The labels below are for the chips, and are never sent.
 */
export const DEFAULT_CONTEXT: MentorContextSelection = {}

export function contextLabels(
  base: MentorContextSelection,
  language: 'ar' | 'en',
  n: (value: number) => string,
  { withCourse = true }: { withCourse?: boolean } = {},
): { lesson: string | null; code: string | null } {
  // With the course picker beside it, the lesson chip need not name the course again.
  const lesson = base.lessonId
    ? [withCourse ? base.courseTitle : null, base.lessonNumber ? (language === 'ar' ? `الدرس ${n(base.lessonNumber)}` : `Lesson ${base.lessonNumber}`) : null, base.lessonTitle]
        .filter(Boolean).join(' · ')
    : null
  const code = base.exerciseId ? (base.exerciseTitle || (language === 'ar' ? 'تمرين الكود' : 'Code exercise')) : null
  return { lesson, code }
}

/**
 * What the mentor hub attaches: the whole course (its id, its name and whether the learner is
 * enrolled), never one lesson or exercise in it, even when the server's default or a link resolved
 * one. A single lesson is asked about in that lesson's own mentor panel.
 */
export function wholeCourse({ courseId, courseTitle, courseEnrolled }: MentorContextSelection): MentorContextSelection {
  return { courseId, courseTitle, courseEnrolled }
}

/**
 * The `context` of one request, from the chips that are on: removing a chip removes its ids from
 * the request. An enrolled course the learner chose stays attached when the lesson chip is removed
 * (the conversation is then about the whole course); with nothing left the mentor answers in general.
 */
export function buildContext(base: MentorContextSelection, on: { lesson: boolean; code: boolean }, selectedText?: string): MentorContextRef {
  const context: MentorContextRef = {}
  if (on.lesson && base.lessonId) {
    if (base.courseId) context.courseId = base.courseId
    context.lessonId = base.lessonId
  } else if (base.courseId && base.courseEnrolled) {
    context.courseId = base.courseId
  }
  if (on.code && base.exerciseId) {
    context.exerciseId = base.exerciseId
    context.attachCode = true
  }
  if (selectedText) context.selectedText = selectedText
  return context
}
