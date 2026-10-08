import type { PlanBlock } from './types'

/**
 * Canonical Masar links for what the mentor refers to. The server sends ids (a course slug and a
 * lesson id it has verified); the app builds the URL, so neither the model nor server text ever
 * decides where a link goes.
 */
export function lessonHref(courseId?: string | null, lessonId?: string | null): string | null {
  if (!courseId || !lessonId) return null
  if (!/^\d{1,9}$/.test(lessonId) || !/^[a-z0-9][a-z0-9-]{0,119}$/i.test(courseId)) return null
  return `/courses/${courseId.toLowerCase()}/lessons/${lessonId}`
}

export function planBlockHref(block: PlanBlock): string {
  const lesson = lessonHref(block.courseId, block.lessonId)
  if (lesson) return lesson
  if (block.refId === 'mentor:chat') return '/mentor'
  // The design fixtures carry app paths; anything else (or a protocol-relative URL) goes nowhere unexpected.
  if (block.refId.startsWith('/') && !block.refId.startsWith('//')) return block.refId
  return '/learn'
}
