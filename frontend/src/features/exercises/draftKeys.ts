import { accountScope } from '@/lib/privateStorage'
import { useAuthStore } from '@/lib/store'

/**
 * Where an exercise draft is kept in this browser: `exercise:<account>:<exercise>:<file>`, plus
 * `:starter-<version>` for CodeCell's own copy (a new starter must not be hidden by an old draft).
 * The stable form without the starter is what the mentor's Code Review reads.
 *
 * Keyed by the signed-in account, so another account on the same browser never reads (or sends to
 * a review) a draft it did not write; sign-out also clears them all (lib/privateStorage.ts).
 */
export function exerciseDraftKey(exerciseId: string | number, fileName: string, starter?: string): string {
  const owner = accountScope(useAuthStore.getState().user?.id)
  return `exercise:${owner}:${exerciseId}:${fileName}${starter ? `:starter-${starter}` : ''}`
}
