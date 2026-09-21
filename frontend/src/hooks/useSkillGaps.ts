'use client'
import { useEffect, useState } from 'react'
import { api } from '@/lib/api'
import type { SkillGaps } from '@/types'

export type SkillGapsState =
  | { kind: 'loading' }
  | { kind: 'error' }
  /** The learner has no roadmap yet: nothing to measure against. */
  | { kind: 'unavailable' }
  | { kind: 'ready'; gaps: SkillGaps }

type Settled = Exclude<SkillGapsState, { kind: 'loading' }>

/**
 * The learner's skill gaps, exactly as the backend computed them.
 *
 * `reloadKey` is how a screen says "the roadmap or the skills changed, ask
 * again" (a rebuilt roadmap has a new id; a saved skill list bumps a counter).
 * Nothing is derived here: statuses, groups, counts and the coverage
 * percentage all arrive finished.
 *
 * "Loading" is not stored: an answer is remembered together with the request it
 * answers, and anything that does not answer the current request is loading.
 */
export function useSkillGaps(reloadKey: string | number = 0): SkillGapsState & { retry: () => void } {
  const [attempt, setAttempt] = useState(0)
  const key = `${reloadKey}:${attempt}`
  const [answer, setAnswer] = useState<{ key: string; state: Settled } | null>(null)

  useEffect(() => {
    let alive = true
    ;(async () => {
      let state: Settled
      try {
        const gaps = await api.getMySkillGaps()
        state = gaps.available ? { kind: 'ready', gaps } : { kind: 'unavailable' }
      } catch {
        state = { kind: 'error' }
      }
      if (alive) setAnswer({ key, state })
    })()
    return () => {
      alive = false
    }
  }, [key])

  const state: SkillGapsState = answer && answer.key === key ? answer.state : { kind: 'loading' }
  return { ...state, retry: () => setAttempt((n) => n + 1) }
}
