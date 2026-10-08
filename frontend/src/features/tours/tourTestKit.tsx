import { vi } from 'vitest'
import type { User } from '@/types'
import { useAuthStore } from '@/lib/store'

/**
 * What the tour tests share. jsdom has no layout, so the geometry the tour measures is
 * stood in for here: the overlay is a viewport of a given size, and each `data-tour`
 * element has a rectangle (or none, which is how an element that is not on screen reads).
 */

export interface Rect { x: number; y: number; w: number; h: number }

const DEFAULT_RECT: Rect = { x: 100, y: 100, w: 200, h: 80 }

interface LayoutOptions {
  width?: number
  height?: number
  /** Rectangles by `data-tour` id; anything else gets a default box. */
  rects?: Record<string, Rect>
  /** Rectangles that depend on the document's direction (a sidebar swaps sides in RTL). */
  rtlRects?: Record<string, Rect>
  /** Targets that are in the DOM but not on screen. */
  hidden?: string[]
  /** How tall the card is. */
  cardHeight?: number
}

export function mockLayout({ width = 1440, height = 900, rects = {}, rtlRects = {}, hidden = [], cardHeight = 190 }: LayoutOptions = {}) {
  vi.spyOn(HTMLElement.prototype, 'offsetWidth', 'get').mockImplementation(function (this: HTMLElement) {
    return this.classList.contains('tour-layer') ? width : 344
  })
  vi.spyOn(HTMLElement.prototype, 'offsetHeight', 'get').mockImplementation(function (this: HTMLElement) {
    return this.classList.contains('tour-layer') ? height : cardHeight
  })
  vi.spyOn(Element.prototype, 'getBoundingClientRect').mockImplementation(function (this: Element) {
    const id = this.getAttribute('data-tour')
    let r: Rect | null = null
    if (id) {
      if (hidden.includes(id)) r = null
      else r = (document.documentElement.dir === 'rtl' && rtlRects[id]) || rects[id] || DEFAULT_RECT
    } else if (this.classList.contains('tour-layer')) {
      r = { x: 0, y: 0, w: width, h: height }
    }
    const box = r ?? { x: 0, y: 0, w: 0, h: 0 }
    return { x: box.x, y: box.y, left: box.x, top: box.y, width: box.w, height: box.h, right: box.x + box.w, bottom: box.y + box.h, toJSON: () => ({}) }
  })
  // The page is asked to scroll a target into view; there is no page to scroll.
  window.scrollTo = vi.fn()
}

export const student = (over: Partial<User> = {}): User => ({
  id: 7, email: 'layan@example.com', full_name: 'Layan Harbi', role: 'student', experience_level: 'beginner',
  is_verified: true, overall_readiness_score: 42, created_at: '2026-10-11T09:00:00Z',
  requires_legal_acceptance: false, pending_updates: [], ...over,
})

/** An account that signed up before the walkthroughs shipped. */
export const OLD_ACCOUNT = '2026-03-01T00:00:00Z'

export function signIn(over: Partial<User> = {}): User {
  const user = student(over)
  useAuthStore.setState({ token: 'tok', expiresAt: null, _hasHydrated: true, user })
  return user
}

export function Targets({ ids }: { ids: readonly string[] }) {
  return <div>{ids.map((id) => <div key={id} data-tour={id}>{id}</div>)}</div>
}

export const ONBOARDING_DESKTOP = ['path', 'learn', 'nav-practice', 'nav-mentor']
export const ONBOARDING_MOBILE = ['path', 'learn', 'practice', 'mentor']
