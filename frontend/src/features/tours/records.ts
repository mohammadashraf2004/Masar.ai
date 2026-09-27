import type { TourId } from './registry'

/**
 * What each account has done with each tour.
 *
 * There is no endpoint for it yet, so it lives in this browser (`masar.tours`, keyed by
 * account so two people on one machine do not inherit each other's), and a tour a person
 * finished on another device is shown again here. The backend request in
 * docs/backend-requests.md moves it onto the profile; only this file changes then.
 */

export type TourStatus = 'done' | 'skipped'

export interface TourRecord {
  status: TourStatus
  /** The tour's version when it was seen; a later version is shown again. */
  version: number
  /** ISO time. */
  at: string
}

export const TOURS_STORAGE_KEY = 'masar.tours'

type Store = Record<string, Partial<Record<TourId, TourRecord>>>

function read(): Store {
  try {
    const parsed: unknown = JSON.parse(window.localStorage.getItem(TOURS_STORAGE_KEY) ?? '{}')
    return parsed && typeof parsed === 'object' && !Array.isArray(parsed) ? (parsed as Store) : {}
  } catch {
    return {}
  }
}

export function getRecord(userId: number, tour: TourId): TourRecord | undefined {
  const rec = read()[String(userId)]?.[tour]
  return rec && (rec.status === 'done' || rec.status === 'skipped') && typeof rec.version === 'number' ? rec : undefined
}

export function saveRecord(userId: number, tour: TourId, rec: Omit<TourRecord, 'at'> & { at?: string }): void {
  const all = read()
  all[String(userId)] = { ...all[String(userId)], [tour]: { ...rec, at: rec.at ?? new Date().toISOString() } }
  try {
    window.localStorage.setItem(TOURS_STORAGE_KEY, JSON.stringify(all))
  } catch {
    // Storage is blocked or full: the tour is simply shown again next time.
  }
}
