import type { StringKey } from '@/lib/i18n'

/**
 * The walkthroughs, as data. Adding a tour or a step is an entry here plus a
 * `data-tour="…"` on the element it points at; there is no layout work.
 */

export type TourId = 'onboarding' | 'mentor-interview' | 'language'
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
}

/**
 * When the walkthroughs shipped. An account created before it is an "existing" one: it
 * sees feature tours with the "New" tag and is not given the first-run onboarding; one
 * created after it is a new signup, and gets the opposite. Set this to the real release
 * date when it ships.
 */
// TODO(product): set real release date
export const TOURS_RELEASED_AT = '2026-09-27T00:00:00Z'

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
    id: 'mentor-interview',
    version: 1,
    route: '/mentor',
    kind: 'feature',
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
