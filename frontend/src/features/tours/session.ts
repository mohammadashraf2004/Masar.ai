/**
 * "Never two tours in one session."
 *
 * A session is the browser tab's: `sessionStorage` survives a reload but not a new tab or
 * a new visit, which is the granularity the rule wants (finish the first-run tour, reload,
 * and the next tour still waits). A module variable backs it where storage is unavailable.
 *
 * Also here: the switch that turns tours off (the test suite does, so a tour never appears
 * over an unrelated test) and the replay that survives a route change.
 */

const SESSION_KEY = 'masar.tours.session'

let ranInMemory = false
let enabled = true
let pendingReplay: string | null = null

export function tourRanThisSession(): boolean {
  if (ranInMemory) return true
  try {
    return window.sessionStorage.getItem(SESSION_KEY) === '1'
  } catch {
    return false
  }
}

export function markTourSession(): void {
  ranInMemory = true
  try {
    window.sessionStorage.setItem(SESSION_KEY, '1')
  } catch {
    // Kept in memory only.
  }
}

export function resetTourSession(): void {
  ranInMemory = false
  pendingReplay = null
  try {
    window.sessionStorage.removeItem(SESSION_KEY)
  } catch {
    // Nothing to clear.
  }
}

export function toursEnabled(): boolean {
  return enabled
}

export function setToursEnabled(value: boolean): void {
  enabled = value
}

/** "Replay tour" from a page the tour is not on: go there, then start it. */
export function setPendingReplay(id: string | null): void {
  pendingReplay = id
}

export function peekPendingReplay(): string | null {
  return pendingReplay
}

export function clearPendingReplay(): void {
  pendingReplay = null
}
