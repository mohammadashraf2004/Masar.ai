'use client'
import { useEffect, useRef, useState } from 'react'

/**
 * The height that takes an element from where it starts on the page to the bottom of the window
 * (less `gap`), never under `min`: the mentor's chat window then fills a small laptop and a large
 * monitor alike, its composer in view, instead of one fixed height for every screen.
 *
 * Measured as if the page were scrolled to the top, so it follows whatever sits above the element
 * (a header that wraps in another language included), and again when the window or the page's
 * scroll pane is resized. Undefined until measured: the caller keeps a fallback height for the
 * first paint and for the server render.
 *
 * Returns `[ref, height]` - two values rather than one object, so the height is never read off
 * something holding a ref while rendering.
 */
export function useFillHeight<T extends HTMLElement>({ min = 420, gap = 20 }: { min?: number; gap?: number } = {}) {
  const ref = useRef<T>(null)
  const [height, setHeight] = useState<number | undefined>(undefined)

  useEffect(() => {
    const element = ref.current
    if (!element) return
    // On a wide screen the page scrolls inside its pane (`PageBody`), below that the window scrolls.
    const pane = element.closest<HTMLElement>('[data-page-scroll]')
    const measure = () => {
      const top = element.getBoundingClientRect().top + window.scrollY + (pane?.scrollTop ?? 0)
      setHeight(Math.max(min, Math.round(window.innerHeight - top - gap)))
    }
    measure()
    window.addEventListener('resize', measure)
    const observer = typeof ResizeObserver === 'undefined' ? null : new ResizeObserver(measure)
    if (pane) observer?.observe(pane)
    return () => {
      window.removeEventListener('resize', measure)
      observer?.disconnect()
    }
  }, [min, gap])

  return [ref, height] as const
}
