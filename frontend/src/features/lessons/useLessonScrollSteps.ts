import { useEffect, useRef, useState } from 'react'

export type LessonStep = 'content' | 'exercise'

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
      { root, threshold: 0, rootMargin: '0px 0px -85% 0px' },
    )
    observer.observe(target)
    return () => observer.disconnect()
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [hasExercise])

  function scrollTo(step: LessonStep) {
    const root = containerRef.current
    if (!root) return
    setActive(step)
    if (step === 'content') {
      root.scrollTo({ top: 0, behavior: 'smooth' })
      return
    }
    markRead()
    const el = dividerRef.current
    if (!el) return
    const delta = el.getBoundingClientRect().top - root.getBoundingClientRect().top
    // Keep the divider below the sticky content/exercise switcher instead of
    // letting the switcher cover the exercise heading after the jump.
    root.scrollTo({ top: root.scrollTop + delta - 56, behavior: 'smooth' })
  }

  return { containerRef, dividerRef, active, scrollTo }
}
