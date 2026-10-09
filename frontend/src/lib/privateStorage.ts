/**
 * Browser storage that holds one account's private learning data: Mentor v2 conversations and
 * plan, exercise drafts, mock interviews. On a shared browser the next person to sign in must
 * never see any of it, so it is kept two ways:
 *
 * - keyed by the account that wrote it (`accountScope`), so a different account never reads it
 *   even when the first one never signed out (an expired session, a closed tab);
 * - removed on sign-out and whenever the session is dropped (`clearPrivateStorage`, called from
 *   `clearAuth` in lib/store.ts).
 *
 * Deliberately free of imports: lib/store.ts calls it, and the modules that read the signed-in
 * account import lib/store.ts.
 */
export const PRIVATE_STORAGE_PREFIXES = [
  'masar:mentor-v2:',
  // CodeCell drafts and the mentor's read of them (features/exercises/draftKeys.ts). Drafts
  // written before keys carried the account ("exercise:<id>:<file>") are cleared too.
  'exercise:',
  'masar:mock-interviews:',
] as const

/** The account part of a private storage key. */
export function accountScope(userId: number | string | null | undefined): string {
  return userId != null && userId !== '' ? `u${userId}` : 'anon'
}

/** Remove every private key in `storage`, whichever account wrote it. */
export function clearPrivateStorage(storage: Storage): void {
  const keys: string[] = []
  for (let i = 0; i < storage.length; i++) {
    const key = storage.key(i)
    if (key && PRIVATE_STORAGE_PREFIXES.some((prefix) => key.startsWith(prefix))) keys.push(key)
  }
  keys.forEach((key) => storage.removeItem(key))
}
