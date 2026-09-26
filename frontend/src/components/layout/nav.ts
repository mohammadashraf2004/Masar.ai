import type { ElementType } from 'react'
import {
  Award, BarChart3, BookMarked, BookOpen, Compass, CreditCard, Flame, Home, LayoutDashboard, MessageSquareDot, Target, Users, Wrench,
} from 'lucide-react'
import { TrackIcon } from '@/components/brand/TrackIcon'
import type { StringKey } from '@/lib/i18n'

export interface NavItem {
  href: string
  icon: ElementType
  /** An i18n key, not a string: the sidebar is the one piece of chrome on every
   *  page, so it has to follow the reader's language like the content does. */
  label: StringKey
}

/**
 * Where the shell can take you. One list, rendered by the desktop sidebar and
 * by the mobile menu: the two must never drift into offering different
 * destinations.
 *
 * The design handoff draws five (Home, Tracks, Courses, Exercises,
 * Certificates); the product has more, and none of the rest is removed. The five
 * keep the handoff's relative order. "Courses" is the tool courses (`/tools`) and
 * "Exercises" has no page of its own (they live inside lessons), so it is not a
 * destination here.
 */
export const NAV: NavItem[] = [
  { href: '/',             icon: Home,            label: 'nav.home' },
  { href: '/dashboard',    icon: LayoutDashboard, label: 'nav.dashboard' },
  { href: '/learn',        icon: Target,          label: 'nav.learn' },
  { href: '/learn/my-courses', icon: BookOpen,    label: 'nav.myCourses' },
  { href: '/explore',      icon: Compass,         label: 'nav.explore' },
  // The tracks icon is the mark's own two rails and marker, as the handoff draws it.
  { href: '/tracks',       icon: TrackIcon,       label: 'nav.tracks' },
  { href: '/tools',        icon: Wrench,          label: 'nav.tools' },
  { href: '/certificates', icon: Award,           label: 'nav.certificates' },
  // Plans & offers sits right after Certificates, as the handoff orders them.
  { href: '/billing',      icon: CreditCard,      label: 'nav.billing' },
  { href: '/glossary',     icon: BookMarked,      label: 'nav.glossary' },
  // A speech bubble with a dot in it, as the handoff draws the mentor.
  { href: '/mentor',       icon: MessageSquareDot, label: 'nav.mentor' },
  { href: '/community',    icon: Users,           label: 'nav.community' },
  { href: '/challenges',   icon: Flame,           label: 'nav.challenges' },
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
