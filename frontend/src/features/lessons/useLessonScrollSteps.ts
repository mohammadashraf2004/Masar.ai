import { useEffect, useRef, useState } from 'react'

export type LessonStep = 'content' | 'exercise'

// Where the sticky step bar ends once stuck, so a jump or a focused editor
// line lands below it rather than under it. A plain function of the DOM (not
// a closure over render state), so effects can call it without depending on it.
function measureStickyOffset(container: HTMLElement | null, ownScroll: boolean) {
  const bar = container?.querySelector<HTMLElement>('[data-testid="lesson-step-switcher"]')
  if (!container || !bar) return 64
  // Inside a scroll container a sticky element is offset from its padding
  // edge, so the container's own top padding counts too.
  const padding = ownScroll ? parseFloat(getComputedStyle(container).paddingTop) || 0 : 0
  return padding + (parseFloat(getComputedStyle(bar).top) || 0) + bar.offsetHeight + 8
}

/**
 * Scroll wiring for the content/exercise step switch. Everything scrolls
 * inside the page's own container (`containerRef`), never the window — the
 * desktop app shell locks `<main>` to `overflow-hidden` and gives every page
 * its own `overflow-y-auto` region (see `AppShellFrame`), so `window.scrollTo`
 * or `scrollIntoView` would silently do nothing on desktop.
 *
 * The active pill is driven by an `IntersectionObserver` on the divider
 * between the article and the exercise, scoped to that same container via
 * `root`, so it tracks manual scrolling as well as the pill clicks.
 */
export function useLessonScrollSteps({
  hasExercise,
  onContentRead,
}: {
  hasExercise: boolean
  onContentRead?: () => void
}) {
  const containerRef = useRef<HTMLDivElement>(null)
  const dividerRef = useRef<HTMLDivElement>(null)
  const [active, setActive] = useState<LessonStep>('content')
  const readFired = useRef(false)

  function markRead() {
    if (readFired.current) return
    readFired.current = true
    onContentRead?.()
  }

  // From lg up the page scrolls inside `containerRef`; below it the window
  // scrolls (the container only clips sideways), so scrolling and the
  // observer must use the window there.
  const [ownScroll, setOwnScroll] = useState(true)
  useEffect(() => {
    if (typeof window.matchMedia !== 'function') return
    const query = window.matchMedia('(min-width: 1024px)')
    const update = () => setOwnScroll(query.matches)
    update()
    query.addEventListener?.('change', update)
    return () => query.removeEventListener?.('change', update)
  }, [])

  function stickyOffset() {
    return measureStickyOffset(containerRef.current, ownScroll)
  }

  useEffect(() => {
    if (!hasExercise || ownScroll) return
    // The window scrolls here, so the scroll padding belongs to the document.
    const html = document.documentElement
    const previous = html.style.scrollPaddingTop
    html.style.scrollPaddingTop = `${measureStickyOffset(containerRef.current, ownScroll)}px`
    return () => { html.style.scrollPaddingTop = previous }
  }, [hasExercise, ownScroll])

  useEffect(() => {
    if (!hasExercise) return
    const root = containerRef.current
    const target = dividerRef.current
    if (!root || !target) return

    const observer = new IntersectionObserver(
      ([entry]) => {
        // `threshold: 0` alone only reports enter/exit of the container's
        // full bounds — once the divider is anywhere on screen it stays
        // "intersecting" for the rest of the scroll, so the callback never
        // fires again as it settles near the top. Shrinking the observed
        // region to a thin band at the container's own top edge (via
        // `rootMargin`) makes intersection mean "scrolled up near the top",
        // which is what "passed" actually needs, and re-fires continuously
        // as that band is crossed — on a manual scroll or a `scrollTo` jump.
        setActive(entry.isIntersecting ? 'exercise' : 'content')
        if (entry.isIntersecting) markRead()
      },
      { root: ownScroll ? root : null, threshold: 0, rootMargin: '0px 0px -85% 0px' },
    )
    observer.observe(target)
    return () => observer.disconnect()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hasExercise, ownScroll])

  function scrollTo(step: LessonStep) {
    const root = containerRef.current
    if (!root) return
    setActive(step)
    if (step === 'content') {
      if (ownScroll) root.scrollTo({ top: 0, behavior: 'smooth' })
      else window.scrollTo({ top: 0, behavior: 'smooth' })
      return
    }
    markRead()
    const el = dividerRef.current
    if (!el) return
    // Keep the divider below the sticky content/exercise switcher instead of
    // letting the switcher cover the exercise heading after the jump.
    if (!ownScroll) {
      window.scrollTo({ top: window.scrollY + el.getBoundingClientRect().top - stickyOffset(), behavior: 'smooth' })
      return
    }
    const delta = el.getBoundingClientRect().top - root.getBoundingClientRect().top
    root.scrollTo({ top: root.scrollTop + delta - stickyOffset(), behavior: 'smooth' })
  }

  return { containerRef, dividerRef, active, scrollTo }
}
