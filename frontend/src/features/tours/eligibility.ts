import type { User } from '@/types'
import { getRecord } from './records'
import { TOURS, TOURS_RELEASED_AT, routeMatches, tourAvailable, type TourDef } from './registry'

/**
 * Which tour, if any, runs on this page for this account. Pure decisions; nothing here
 * touches the DOM.
 */

// An ISO timestamp with no zone designator is read as UTC, not as the browser's local time,
// so the boundary is the same instant for every learner (the API sends offsets anyway).
const HAS_ZONE = /(Z|[+-]\d{2}:?\d{2})$/i
function parseInstant(value: string): number {
  const text = String(value ?? '').trim()
  return Date.parse(/T\d/.test(text) && !HAS_ZONE.test(text) ? `${text}Z` : text)
}

/** An account created at or after the launch instant. An unreadable date counts as an old one. */
export function isNewAccount(user: Pick<User, 'created_at'>): boolean {
  return parseInstant(user.created_at) >= Date.parse(TOURS_RELEASED_AT)
}

/** Whether a tour is meant for this account at all. */
export function appliesTo(tour: TourDef, user: Pick<User, 'created_at'>): boolean {
  return tour.audience !== 'new-accounts' || isNewAccount(user)
}

/** Whether the "New" tag belongs on this tour's card: a feature, shown to an account that predates it. */
export function showsNewTag(tour: TourDef, user: Pick<User, 'created_at'>): boolean {
  return tour.kind === 'feature' && !isNewAccount(user)
}

function prerequisitesMet(tour: TourDef, user: User, records: typeof getRecord): boolean {
  return (tour.after ?? []).every((id) => {
    const before = TOURS.find((t) => t.id === id)
    // A tour that does not apply to this account is not something it can be waiting for.
    return !before || !appliesTo(before, user) || records(user.id, id) !== undefined
  })
}

/**
 * The first tour whose route this is, that the account has not seen at its current
 * version, that applies to it, and whose predecessors are done. Nothing at all when a
 * tour has already run this session.
 */
export function pickTour(
  pathname: string,
  user: User,
  sessionRan: boolean,
  records: typeof getRecord = getRecord,
): TourDef | null {
  if (sessionRan) return null
  return TOURS.find((tour) =>
    routeMatches(tour, pathname)
    && tourAvailable(tour)
    && appliesTo(tour, user)
    && records(user.id, tour.id)?.version !== tour.version
    && prerequisitesMet(tour, user, records),
  ) ?? null
}

/** Where a tour must never start: over a payment, an exam, or a sign-in. */
const NEVER_ON = ['/billing', '/exam', '/auth', '/onboarding']

export function blockedRoute(pathname: string): boolean {
  return NEVER_ON.some((prefix) => pathname === prefix || pathname.startsWith(prefix + '/'))
}

/** Whether something else is modal right now (an announcement, the terms, a lightbox). */
export function modalOpen(doc: Document = document): boolean {
  return doc.querySelector('[role="dialog"][aria-modal="true"]:not([data-tour-card])') !== null
}
