'use client'
import { useCallback, useRef } from 'react'
import { api } from '@/lib/api'
import { useAuthStore } from '@/lib/store'

/**
 * Returns a function that acknowledges one announcement, once.
 *
 * The announcement leaves the stored account at once, so the dialog closes and
 * cannot reopen while the request is in flight; the server's answer then
 * replaces the list (acknowledging What's New also closes the introduction it
 * covers). A second call while one is running does nothing.
 *
 * If the request fails nothing breaks and nothing is retried: the learner has
 * dismissed it, navigation still works, and because the server never heard, the
 * announcement is offered again the next time they sign in - not forever, and
 * not in this session.
 */
export function useAcknowledgeUpdate(releaseId: string) {
  const started = useRef(false)
  return useCallback(() => {
    if (started.current) return
    started.current = true

    const { user } = useAuthStore.getState()
    if (user?.pending_updates) {
      useAuthStore.setState({ user: { ...user, pending_updates: user.pending_updates.filter((id) => id !== releaseId) } })
    }

    void api.acknowledgeUpdate(releaseId)
      .then((updated) => {
        const current = useAuthStore.getState().user
        // Only the list is taken from the answer, and only for the same account:
        // a sign-out and sign-in in between must not be overwritten.
        if (current && current.id === updated.id) {
          useAuthStore.setState({ user: { ...current, pending_updates: updated.pending_updates ?? [] } })
        }
      })
      .catch(() => { /* see above */ })
  }, [releaseId])
}
