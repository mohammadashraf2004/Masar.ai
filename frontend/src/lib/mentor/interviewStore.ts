import type { InterviewSession } from '@/lib/mentor/interview'
import { accountScope } from '@/lib/privateStorage'
import { useAuthStore } from '@/lib/store'

/**
 * Where mock interviews are kept, for the report page, the "your earlier interviews" list and
 * "retry weak questions".
 *
 * The backend saves nothing: `/mentor/mock-interview` writes a question and forgets it. So the
 * only implementation is `MockInterviewStore`, which keeps them in this browser (see
 * docs/backend-requests.md). The page never touches storage itself, so a real store is a new
 * implementation of this interface, not a change to the screens.
 */
export interface InterviewStore {
  /** Newest first. */
  list(): InterviewSession[]
  get(id: string): InterviewSession | null
  /** The interview that was started and not ended, if any (what a reload resumes). */
  active(): InterviewSession | null
  save(session: InterviewSession): void
  subscribe(listener: () => void): () => void
  /** A string that changes whenever the stored interviews do, for `useSyncExternalStore`. */
  snapshot(): string
}

/** The learner's answers are private: kept per account, and cleared on sign-out (lib/privateStorage.ts). */
const key = () => `masar:mock-interviews:v1:${accountScope(useAuthStore.getState().user?.id)}`
const KEEP = 20
const EMPTY = '[]'

function isSession(value: unknown): value is InterviewSession {
  const s = value as Partial<InterviewSession> | null
  return !!s && typeof s.id === 'string' && typeof s.role === 'string' && Array.isArray(s.questions)
}

export function parseInterviews(raw: string): InterviewSession[] {
  try {
    const value: unknown = JSON.parse(raw)
    return Array.isArray(value) ? value.filter(isSession) : []
  } catch {
    return []
  }
}

/** Interviews kept in localStorage; storage that is blocked or full just means nothing is kept. */
export class MockInterviewStore implements InterviewStore {
  private listeners = new Set<() => void>()

  snapshot(): string {
    try {
      return window.localStorage.getItem(key()) ?? EMPTY
    } catch {
      return EMPTY
    }
  }

  list(): InterviewSession[] {
    return parseInterviews(this.snapshot())
  }

  get(id: string): InterviewSession | null {
    return this.list().find((s) => s.id === id) ?? null
  }

  active(): InterviewSession | null {
    return this.list().find((s) => s.endedAt === null) ?? null
  }

  save(session: InterviewSession): void {
    const others = this.list().filter((s) => s.id !== session.id)
    const next = [session, ...others]
      .sort((a, b) => b.startedAt.localeCompare(a.startedAt))
      .slice(0, KEEP)
    try {
      window.localStorage.setItem(key(), JSON.stringify(next))
    } catch {
      return
    }
    this.listeners.forEach((listener) => listener())
  }

  subscribe(listener: () => void): () => void {
    this.listeners.add(listener)
    const onStorage = (e: StorageEvent) => {
      if (e.key === key() || e.key === null) listener()
    }
    window.addEventListener('storage', onStorage)
    return () => {
      this.listeners.delete(listener)
      window.removeEventListener('storage', onStorage)
    }
  }
}

export const interviewStore: InterviewStore = new MockInterviewStore()

export function newInterviewId(): string {
  const c = typeof globalThis !== 'undefined' ? globalThis.crypto : undefined
  if (c && typeof c.randomUUID === 'function') return c.randomUUID()
  return `iv-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 10)}`
}
