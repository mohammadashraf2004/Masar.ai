'use client'
import { useMemo, useSyncExternalStore } from 'react'
import type { InterviewSession } from '@/lib/mentor/interview'
import { interviewStore, parseInterviews } from '@/lib/mentor/interviewStore'

/**
 * The saved interviews, newest first. Empty on the server and on the first client render, so
 * the two agree; then whatever this browser has. `null` for `loaded` says which of the two an
 * empty list is, so a page can tell "not read yet" from "none".
 */
export function useInterviews(): { interviews: InterviewSession[]; loaded: boolean } {
  const raw = useSyncExternalStore(
    (listener) => interviewStore.subscribe(listener),
    () => interviewStore.snapshot(),
    () => null,
  )
  return useMemo(
    () => (raw === null ? { interviews: [], loaded: false } : { interviews: parseInterviews(raw), loaded: true }),
    [raw],
  )
}
