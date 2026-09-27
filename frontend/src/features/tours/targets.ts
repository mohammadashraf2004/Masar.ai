import { targetFor, type Device, type TourDef, type TourStep } from './registry'

/**
 * Finding what a step points at, and bringing it into view.
 */

/** The steps' fewest that make a tour worth running. */
export const MIN_STEPS = 2

function visible(el: Element): boolean {
  const r = el.getBoundingClientRect()
  return r.width > 0 && r.height > 0
}

/**
 * The element carrying `data-tour="id"`. The same id can be on several (the language
 * switch is in the header and in the phone menu), and one of them is usually hidden, so
 * the first one that is actually on screen wins.
 */
export function findTarget(id: string, root: ParentNode = document): HTMLElement | null {
  const all = Array.from(root.querySelectorAll<HTMLElement>(`[data-tour="${id}"]`))
  return all.find(visible) ?? null
}

/**
 * The steps whose targets are on screen right now, in order. A step whose target is not
 * there is left out silently; the caller decides whether what remains is enough to run.
 */
export function resolveSteps(tour: TourDef, device: Device, root: ParentNode = document): TourStep[] {
  return tour.steps.filter((step) => findTarget(targetFor(step, device), root) !== null)
}

// ─── Scrolling into view ─────────────────────────────────────────────────

function scrollParent(el: HTMLElement): HTMLElement | null {
  for (let p = el.parentElement; p && p !== document.body; p = p.parentElement) {
    if (p.scrollHeight > p.clientHeight + 1 && /auto|scroll/.test(getComputedStyle(p).overflowY)) return p
  }
  return null
}

/** How far down a sticky or fixed header covers the top of the page. */
function headerInset(): number {
  let inset = 0
  document.querySelectorAll('header').forEach((h) => {
    const pos = getComputedStyle(h).position
    if (pos === 'sticky' || pos === 'fixed') inset = Math.max(inset, h.getBoundingClientRect().bottom)
  })
  return inset
}

/**
 * Scroll the target's nearest scrollable parent (or the page) so the card can be beside it.
 * On a phone the target goes 16px from the top (below a sticky header), leaving the rest of
 * the screen for the card; elsewhere it is only brought in if it is not already in view.
 */
export function reveal(el: HTMLElement, compact: boolean): void {
  const parent = scrollParent(el)
  const e = el.getBoundingClientRect()
  const scrollTop = parent ? parent.scrollTop : window.scrollY
  const view = parent ? parent.clientHeight : window.innerHeight
  const originTop = parent ? parent.getBoundingClientRect().top : 0
  const top = e.top - originTop + scrollTop
  const max = (parent ? parent.scrollHeight : document.documentElement.scrollHeight) - view

  let to: number
  if (compact) {
    to = Math.min(top - 16 - (parent ? 0 : headerInset()), max)
    if (Math.abs(scrollTop - to) < 2) return
  } else {
    const inset = parent ? 0 : headerInset()
    if (top >= scrollTop + inset + 8 && top + e.height <= scrollTop + view - 8) return
    to = top - Math.max(16 + inset, (view - e.height) / 3)
  }
  const target = Math.max(0, to)
  if (parent) parent.scrollTo?.({ top: target, behavior: 'smooth' })
  else window.scrollTo({ top: target, behavior: 'smooth' })
}
