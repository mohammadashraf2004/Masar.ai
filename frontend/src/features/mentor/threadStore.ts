import { useAuthStore } from '@/lib/store'
import type { MentorMessageV2 } from './types'

/**
 * Where a Mentor v2 conversation is shown from in this browser, so a question asked in the lesson
 * panel is the same thread the hub chat shows for that lesson. The server keeps the authoritative
 * history; this is the display copy.
 *
 * Keyed by account and by scope, the same rule the server uses for history: one thread per lesson
 * (`lesson:<id>`) and one `general` thread. So a lesson's thread never shows under another lesson,
 * and one account never sees another's thread on a shared browser (logout also clears them all -
 * see `clearAuth` in lib/store.ts).
 */
export const THREAD_PREFIX = 'masar:mentor-v2:thread'
const KEEP = 60

function store(): Storage | null {
  try { return typeof window !== 'undefined' ? window.localStorage : null } catch { return null }
}

function owner(): string {
  const id = useAuthStore.getState().user?.id
  return id != null ? String(id) : 'anon'
}

/** The thread a request belongs to, from the lesson it carries, else the course it is about. */
export function scopeOf(context: { lessonId?: string; courseId?: string } | null | undefined): string {
  if (context?.lessonId) return `lesson:${context.lessonId}`
  return context?.courseId ? `course:${context.courseId}` : 'general'
}

export function threadKey(scope: string = 'general'): string {
  return `${THREAD_PREFIX}:${owner()}:${scope}`
}

export function loadThread(scope: string = 'general'): MentorMessageV2[] {
  try {
    const parsed = JSON.parse(store()?.getItem(threadKey(scope)) ?? '[]')
    return Array.isArray(parsed) ? (parsed as MentorMessageV2[]) : []
  } catch {
    return []
  }
}

export function saveThread(messages: MentorMessageV2[], scope: string = 'general'): void {
  try { store()?.setItem(threadKey(scope), JSON.stringify(messages.slice(-KEEP))) } catch { /* private mode: kept for this page only */ }
}

/** One scope's thread, or with no scope every mentor thread in this browser (any account). */
export function clearThread(scope?: string): void {
  const storage = store()
  if (!storage) return
  try {
    if (scope) { storage.removeItem(threadKey(scope)); return }
    const keys: string[] = []
    for (let i = 0; i < storage.length; i++) {
      const key = storage.key(i)
      if (key && key.startsWith(THREAD_PREFIX)) keys.push(key)
    }
    keys.forEach((key) => storage.removeItem(key))
  } catch { /* nothing to clear */ }
}
