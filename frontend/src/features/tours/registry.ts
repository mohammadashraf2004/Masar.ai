import { mockInterviewAvailable } from '@/features/mentor/flag'
import type { StringKey } from '@/lib/i18n'

/**
 * The walkthroughs, as data. Adding a tour or a step is an entry here plus a
 * `data-tour="…"` on the element it points at; there is no layout work.
 */

export type TourId = 'onboarding' | 'mentor' | 'mentor-interview' | 'language'
export type TourKind = 'onboarding' | 'feature'
export type Device = 'desktop' | 'mobile'
export type Placement = 'side' | 'bottom' | 'top' | 'left' | 'right'

/** A `data-tour` id, or one per device when the element differs (the sidebar item on
 *  desktop, its on-page equivalent on a phone, where the sidebar is not there). */
export type TourTarget = string | { desktop: string; mobile: string }

export interface TourStep {
  target: TourTarget
  /** `side` puts the card beside the target (nav rails); otherwise it is chosen to fit. */
  placement?: Placement
  titleKey: StringKey
  bodyKey: StringKey
  /** Words that differ on a phone, where the step points at something else (the menu button,
   *  say, for what a desktop finds in the header). Whatever is not named is the same. */
  mobile?: { titleKey?: StringKey; bodyKey?: StringKey }
}

export interface TourDef {
  id: TourId
  /** Bump it to show a tour again to everyone, after a change big enough to warrant it. */
  version: number
  /** Where it runs: an exact path, or a list of them. `*` stands for one path segment. */
  route: string | readonly string[]
  kind: TourKind
  steps: readonly TourStep[]
  /** `new-accounts`: only for accounts created after the tours shipped (an older account
   *  has already found its way around, so it never gets the first-run tour). */
  audience?: 'new-accounts'
  /** Tours that come first. Met once they have a saved record, or do not apply to the account. */
  after?: readonly TourId[]
  /** Whether what it shows is open yet. A tour of something not available never runs. */
  available?: () => boolean
}

/**
 * When the walkthroughs shipped. An account created before it is an "existing" one: it
 * sees feature tours with the "New" tag and is not given the first-run onboarding; one
 * created at or after it is a new signup, and gets the opposite.
 */
// The new Masar launch: the start of 10 October 2026 in Cairo. Egypt is on summer time
// (UTC+3) until the last Thursday of October, so this instant is 2026-10-09T21:00:00Z.
// Written with its offset so no runtime timezone can move the boundary.
export const TOURS_RELEASED_AT = '2026-10-10T00:00:00+03:00'

export const TOURS: readonly TourDef[] = [
  {
    id: 'onboarding',
    version: 1,
    route: '/dashboard',
    kind: 'onboarding',
    audience: 'new-accounts',
    steps: [
      { target: 'path', titleKey: 'tour.onboarding.path.title', bodyKey: 'tour.onboarding.path.body' },
      { target: 'learn', titleKey: 'tour.onboarding.learn.title', bodyKey: 'tour.onboarding.learn.body' },
      {
        target: { desktop: 'nav-practice', mobile: 'practice' },
        placement: 'side',
        titleKey: 'tour.onboarding.practice.title',
        bodyKey: 'tour.onboarding.practice.body',
      },
      {
        target: { desktop: 'nav-mentor', mobile: 'mentor' },
        placement: 'side',
        titleKey: 'tour.onboarding.mentor.title',
        bodyKey: 'tour.onboarding.mentor.body',
      },
    ],
  },
  {
    // How to use the mentor hub, before its newer feature tours (the first tour on a route runs).
    id: 'mentor',
    version: 1,
    route: '/mentor',
    kind: 'feature',
    steps: [
      { target: 'mentor-course', placement: 'bottom', titleKey: 'tour.mentor.course.title', bodyKey: 'tour.mentor.course.body' },
      { target: 'mentor-context', placement: 'bottom', titleKey: 'tour.mentor.context.title', bodyKey: 'tour.mentor.context.body' },
      { target: 'mentor-actions', placement: 'top', titleKey: 'tour.mentor.actions.title', bodyKey: 'tour.mentor.actions.body' },
      { target: 'mentor-composer', placement: 'top', titleKey: 'tour.mentor.composer.title', bodyKey: 'tour.mentor.composer.body' },
      // Beside the chat on a desktop; a phone has no room for it, so the step is skipped there.
      { target: 'mentor-learner', titleKey: 'tour.mentor.learner.title', bodyKey: 'tour.mentor.learner.body' },
      // On a phone the chat covers the whole screen and the tabs sit under it: there is nothing
      // to point at (`mentor-tabs-phone` is on no element), so the step is skipped.
      {
        target: { desktop: 'mentor-tabs', mobile: 'mentor-tabs-phone' },
        placement: 'bottom',
        titleKey: 'tour.mentor.tabs.title',
        bodyKey: 'tour.mentor.tabs.body',
      },
    ],
  },
  {
    id: 'mentor-interview',
    version: 1,
    route: '/mentor',
    kind: 'feature',
    available: mockInterviewAvailable,
    steps: [
      { target: 'interview-tab', titleKey: 'tour.interview.tab.title', bodyKey: 'tour.interview.tab.body' },
      { target: 'credits', titleKey: 'tour.interview.credits.title', bodyKey: 'tour.interview.credits.body' },
    ],
  },
  {
    id: 'language',
    version: 1,
    // A lesson (a curriculum course's, or a tool course's) or the mentor: whichever comes first.
    route: ['/courses/*/learn', '/tools/*', '/mentor'],
    kind: 'feature',
    after: ['onboarding'],
    steps: [
      {
        // On a phone the switch is inside the menu, which a tour never opens: it points at the button that opens it.
        target: { desktop: 'lang-switch', mobile: 'menu-button' },
        placement: 'bottom',
        titleKey: 'tour.language.switch.title',
        bodyKey: 'tour.language.switch.body',
        mobile: { bodyKey: 'tour.language.switch.mobile.body' },
      },
      { target: 'lesson-terms', titleKey: 'tour.language.terms.title', bodyKey: 'tour.language.terms.body' },
      { target: 'mentor-lang', placement: 'side', titleKey: 'tour.language.mentor.title', bodyKey: 'tour.language.mentor.body' },
    ],
  },
]

export function tourAvailable(tour: TourDef): boolean {
  return tour.available?.() ?? true
}

export function tourById(id: TourId): TourDef {
  const tour = TOURS.find((t) => t.id === id)
  if (!tour) throw new Error(`unknown tour: ${id}`)
  return tour
}

/** The `data-tour` id a step points at on this device. */
export function targetFor(step: TourStep, device: Device): string {
  return typeof step.target === 'string' ? step.target : step.target[device]
}

/** The i18n keys of a step's title and body on this device. */
export function copyFor(step: TourStep, device: Device): { titleKey: StringKey; bodyKey: StringKey } {
  const override = device === 'mobile' ? step.mobile : undefined
  return { titleKey: override?.titleKey ?? step.titleKey, bodyKey: override?.bodyKey ?? step.bodyKey }
}

function routes(tour: TourDef): readonly string[] {
  return typeof tour.route === 'string' ? [tour.route] : tour.route
}

/** Whether `pathname` is one of the tour's routes. A trailing slash is ignored. */
export function routeMatches(tour: TourDef, pathname: string): boolean {
  const path = pathname.replace(/\/+$/, '') || '/'
  return routes(tour).some((pattern) => {
    const a = pattern.split('/')
    const b = path.split('/')
    return a.length === b.length && a.every((seg, i) => seg === '*' ? b[i] !== '' : seg === b[i])
  })
}

/** Where to send someone to replay this tour. */
export function homeRoute(tour: TourDef): string {
  return routes(tour)[0]
}
