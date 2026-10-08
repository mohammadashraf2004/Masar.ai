import type { ElementType } from 'react'
import {
  BarChart3, BookMarked, Compass, Flame, Home, MessageSquareDot, Target, Users, Wrench,
} from 'lucide-react'
import { TrackIcon } from '@/components/brand/TrackIcon'
import type { StringKey } from '@/lib/i18n'

export interface NavItem {
  href: string
  icon: ElementType
  /** An i18n key, not a string: the sidebar is the one piece of chrome on every
   *  page, so it has to follow the reader's language like the content does. */
  label: StringKey
  /** The walkthrough's handle for this item (`data-tour`), where a tour points at it. */
  tour?: string
  /** Starts a new visual group (a divider before it), for MAIN / LEARNING / RESOURCES. */
  groupStart?: boolean
}

/**
 * Where the shell can take you. One list, rendered by the desktop sidebar and
 * by the mobile menu: the two must never drift into offering different
 * destinations.
 *
 * Consolidated per the navigation IA pass: Dashboard, Learn and My Courses
 * folded into "Your Masar" (`/learn/masar`, the personalised path); Learning
 * Certificates moved into Your Masar's summary card; Credit Wallet and Plans
 * & Offers moved to the top bar. The old routes
 * still resolve (deep links, back-buttons), they are just not primary
 * destinations any more.
 */
export const NAV: NavItem[] = [
  { href: '/',             icon: Home,            label: 'nav.home' },
  { href: '/learn/masar',  icon: Target,          label: 'nav.yourMasar' },
  { href: '/explore',      icon: Compass,         label: 'nav.explore' },
  { href: '/tracks',       icon: TrackIcon,       label: 'nav.tracks' },
  // A speech bubble with a dot in it, as the handoff draws the mentor.
  { href: '/mentor',       icon: MessageSquareDot, label: 'nav.mentor', tour: 'nav-mentor', groupStart: true },
  // The graded challenges are where practice lives (there is no separate Exercises page), so the
  // walkthrough's "practice" step points here.
  { href: '/challenges',   icon: Flame,           label: 'nav.challenges', tour: 'nav-practice' },
  { href: '/community',    icon: Users,           label: 'nav.community' },
  { href: '/tools',        icon: Wrench,          label: 'nav.tools', groupStart: true },
  { href: '/glossary',     icon: BookMarked,      label: 'nav.glossary' },
]

// Appended for admins only. Kept separate from NAV rather than filtered out
// of it, so the ordinary list stays the thing every student sees and an
// admin's extra destination is visibly an addition to it.
//
// This is navigation, not authorization: /admin/analytics checks the role
// itself and every endpoint behind it is guarded by require_admin. Hiding
// the link only avoids offering a student a page that would refuse them.
export const ADMIN_NAV: NavItem[] = [
  { href: '/admin/analytics', icon: BarChart3, label: 'nav.admin' },
]

export function navFor(role: string | undefined): NavItem[] {
  return role === 'admin' ? [...NAV, ...ADMIN_NAV] : NAV
}

/** The current section: the exact page, or anything beneath it. */
export function isActive(pathname: string, href: string): boolean {
  return pathname === href || pathname.startsWith(href + '/')
}
