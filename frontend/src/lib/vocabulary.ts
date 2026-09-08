'use client'
import { create } from 'zustand'
import { api } from '@/lib/api'
import { useAuthStore } from '@/lib/store'

/**
 * English-terminology progress.
 *
 * A term moves through two states:
 *
 *   encountered — the student has seen it introduced in a lesson.
 *   learned     — they have also answered something about it correctly, or
 *                 marked it themselves from the glossary.
 *
 * "Encountered" events fire from lesson rendering, so they arrive in bursts
 * of a dozen per paragraph render. They are queued and flushed once, on a
 * short debounce, rather than one request per term.
 *
 * Every call is best-effort: a signed-out reader, a 401, or a backend that
 * hasn't been migrated yet must not break a lesson. Failures leave the local
 * optimistic state in place and are not retried.
 *
 * Nothing is sent without a token. The API client logs the user out on any
 * 401, so firing vocabulary calls from a public page would bounce a visitor
 * to the login screen for reading a lesson preview.
 */

const FLUSH_DELAY_MS = 1500

interface VocabularyState {
  encountered: Set<string>
  learned: Set<string>
  loaded: boolean
  loading: boolean

  load: () => Promise<void>
  markEncountered: (termIds: string[]) => void
  markLearned: (termId: string) => Promise<void>
}

let flushTimer: ReturnType<typeof setTimeout> | null = null
let pending: string[] = []

function isSignedIn(): boolean {
  const { token, isTokenExpired } = useAuthStore.getState()
  return Boolean(token) && !isTokenExpired()
}

export const useVocabularyStore = create<VocabularyState>()((set, get) => ({
  encountered: new Set<string>(),
  learned: new Set<string>(),
  loaded: false,
  loading: false,

  load: async () => {
    if (get().loaded || get().loading) return
    if (!isSignedIn()) {
      set({ loaded: true })
      return
    }
    set({ loading: true })
    try {
      const progress = await api.getVocabularyProgress()
      set({
        encountered: new Set(progress.encountered),
        learned: new Set(progress.learned),
        loaded: true,
      })
    } catch {
      // Signed out, or the endpoint isn't available — the glossary still
      // renders, it just shows nothing as learned.
      set({ loaded: true })
    } finally {
      set({ loading: false })
    }
  },

  markEncountered: (termIds) => {
    const { encountered } = get()
    const fresh = termIds.filter((id) => id && !encountered.has(id))
    if (fresh.length === 0) return

    // Optimistic: the progress bar should move as the student reads, not
    // after a round-trip.
    const next = new Set(encountered)
    for (const id of fresh) next.add(id)
    set({ encountered: next })

    pending.push(...fresh)
    if (flushTimer) clearTimeout(flushTimer)
    flushTimer = setTimeout(() => {
      const batch = Array.from(new Set(pending))
      pending = []
      flushTimer = null
      if (batch.length === 0 || !isSignedIn()) return
      api.recordVocabulary(batch, 'encountered').catch(() => {})
    }, FLUSH_DELAY_MS)
  },

  markLearned: async (termId) => {
    const { learned, encountered } = get()
    if (learned.has(termId)) return
    set({
      learned: new Set(learned).add(termId),
      encountered: new Set(encountered).add(termId),
    })
    if (!isSignedIn()) return
    try {
      await api.recordVocabulary([termId], 'learned')
    } catch {}
  },
}))

/** Convenience selector for the progress widgets. */
export function vocabularyCounts(state: Pick<VocabularyState, 'encountered' | 'learned'>) {
  return { encountered: state.encountered.size, learned: state.learned.size }
}
