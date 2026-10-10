'use client'
import { useCallback, useEffect, useId, useRef, useState, type CSSProperties } from 'react'
import { createPortal } from 'react-dom'
import { useI18n } from '@/lib/i18n'
import { place, type Box } from './place'
import { copyFor, targetFor, type Device, type TourDef, type TourStep } from './registry'
import { findTarget, reveal } from './targets'
import type { TourStatus } from './records'

/**
 * The walkthrough overlay: a spotlight on the target, the page dimmed around it, and a card
 * that says what it is. The real page stays mounted and keeps scrolling underneath.
 *
 * It is drawn in a portal, in viewport coordinates, and follows its target: the position is
 * measured again on scroll, resize, and any change to the page, and for a moment after each
 * step (the page may still be loading, or scrolling the target into view). When nothing can
 * move it stops measuring.
 */

/** Below this the card is as wide as the screen and goes above or below the target only. */
const COMPACT_WIDTH = 640
const PAD = 6

interface Geometry { r: Box | null; W: number; H: number; ch: number }

const FOCUSABLE = 'button:not([disabled])'

function prefersReducedMotion(): boolean {
  return typeof window.matchMedia === 'function' && window.matchMedia('(prefers-reduced-motion: reduce)').matches
}

export interface TourProps {
  tour: TourDef
  /** The steps to show: the tour's, less any whose target is not on this page. */
  steps: readonly TourStep[]
  /** Which of a step's targets to point at. */
  device: Device
  /** Show the amber "New" tag (a feature tour, for an account that predates it). */
  showNew?: boolean
  onFinish: (status: TourStatus) => void
}

export function Tour({ tour, steps, device, showNew = false, onFinish }: TourProps) {
  const { t, tf, language, dir } = useI18n()
  const titleId = useId()
  const layerRef = useRef<HTMLDivElement>(null)
  const cardRef = useRef<HTMLDivElement>(null)

  const [index, setIndex] = useState(0)
  const [swapping, setSwapping] = useState(false)
  const [geo, setGeo] = useState<Geometry>({ r: null, W: 0, H: 0, ch: 190 })
  const [placed, setPlaced] = useState(false)

  const n = steps.length
  const i = Math.min(index, n - 1)
  const step = steps[i]
  const last = i === n - 1
  const feature = tour.kind === 'feature'

  // What the effects below need to read without being torn down by it changing.
  const live = useRef({ i, step, device, geo })
  useEffect(() => { live.current = { i, step, device, geo } })
  const tracker = useRef<{ wake: (ms: number) => void; search: () => void } | null>(null)

  // ─── Moving between steps ───────────────────────────────────────────────
  const swapTimer = useRef<ReturnType<typeof setTimeout>>()
  const go = useCallback((to: number) => {
    if (swapTimer.current || to < 0 || to >= n || to === live.current.i) return
    if (prefersReducedMotion()) { setIndex(to); return }
    // The text fades out, the step changes underneath it, and the new text fades in.
    setSwapping(true)
    swapTimer.current = setTimeout(() => {
      swapTimer.current = undefined
      setIndex(to)
      setSwapping(false)
    }, 140)
  }, [n])
  useEffect(() => () => clearTimeout(swapTimer.current), [])

  const next = () => (last ? onFinish('done') : go(i + 1))
  const back = () => go(i - 1)
  const skip = () => onFinish('skipped')
  const actions = useRef({ next, back, skip })
  useEffect(() => { actions.current = { next, back, skip } })

  // ─── Following the target ───────────────────────────────────────────────
  useEffect(() => {
    let raf = 0
    let until = 0
    let heartbeat: ReturnType<typeof setInterval> | undefined
    let placeTimer: ReturnType<typeof setTimeout> | undefined
    let found = false
    let seen = -1
    let revealUntil = 0
    let revealing = false

    const measure = () => {
      const layer = layerRef.current
      if (!layer) return
      const W = layer.offsetWidth, H = layer.offsetHeight
      if (!W) return
      const { i: at, step: current, device: dev, geo: prev } = live.current
      const el = findTarget(targetFor(current, dev))
      if (seen !== at) { seen = at; revealUntil = Date.now() + 1500 }
      if (el && Date.now() < revealUntil && !revealing) {
        revealing = true
        reveal(el, W < COMPACT_WIDTH)
        setTimeout(() => { revealing = false }, 250)
      }
      let r: Box | null = null
      if (el) {
        found = true
        const origin = layer.getBoundingClientRect(), b = el.getBoundingClientRect()
        r = { x: b.left - origin.left, y: b.top - origin.top, w: b.width, h: b.height }
      }
      const ch = cardRef.current ? cardRef.current.offsetHeight : prev.ch
      const differs = (a: number, b: number) => Math.abs(a - b) > 0.5
      const moved = (!r) !== (!prev.r) || (r && prev.r && (differs(r.x, prev.r.x) || differs(r.y, prev.r.y) || differs(r.w, prev.r.w) || differs(r.h, prev.r.h)))
      if (r && !placeTimer) placeTimer = setTimeout(() => setPlaced(true), 60)
      if (moved || W !== prev.W || H !== prev.H || differs(ch, prev.ch)) setGeo({ r, W, H, ch })
    }

    // Measure every frame, but only while something can move.
    const wake = (ms: number) => {
      until = Math.max(until, Date.now() + ms)
      if (raf) return
      const loop = () => {
        if (Date.now() > until) { raf = 0; return }
        measure()
        raf = requestAnimationFrame(loop)
      }
      raf = requestAnimationFrame(loop)
    }
    // Retry about every 400ms until the target is on the page: it may mount late.
    const search = () => {
      found = false
      if (heartbeat) return
      heartbeat = setInterval(() => {
        if (found) { clearInterval(heartbeat); heartbeat = undefined } else wake(300)
      }, 400)
    }
    tracker.current = { wake, search }

    const onMove = () => wake(400)
    document.addEventListener('scroll', onMove, true)
    window.addEventListener('resize', onMove)
    const observers: Array<{ disconnect: () => void }> = []
    if (typeof ResizeObserver === 'function') {
      const ro = new ResizeObserver(onMove)
      ro.observe(document.documentElement)
      observers.push(ro)
    }
    if (typeof MutationObserver === 'function') {
      const mo = new MutationObserver(() => wake(600))
      mo.observe(document.body, { childList: true, subtree: true })
      observers.push(mo)
    }

    search()
    wake(5000)
    // If the target never turns up the card is centred over a full dim, rather than never shown.
    const fallback = setTimeout(() => setPlaced(true), 2500)

    return () => {
      cancelAnimationFrame(raf)
      clearInterval(heartbeat)
      clearTimeout(placeTimer)
      clearTimeout(fallback)
      document.removeEventListener('scroll', onMove, true)
      window.removeEventListener('resize', onMove)
      observers.forEach((o) => o.disconnect())
      tracker.current = null
    }
  }, [])

  // A new step, or a new language (the page flips direction and the card changes size), moves things.
  useEffect(() => {
    tracker.current?.search()
    tracker.current?.wake(1800)
  }, [i, language, device])

  // ─── Keyboard and focus ─────────────────────────────────────────────────
  useEffect(() => {
    const previous = document.activeElement instanceof HTMLElement ? document.activeElement : null
    cardRef.current?.focus({ preventScroll: true })
    return () => { if (previous && previous.isConnected) previous.focus({ preventScroll: true }) }
  }, [])

  useEffect(() => {
    // Forward is the arrow that points the way the text reads: ← in RTL, → in LTR.
    const forward = dir === 'rtl' ? 'ArrowLeft' : 'ArrowRight'
    const backward = dir === 'rtl' ? 'ArrowRight' : 'ArrowLeft'

    const onKey = (e: KeyboardEvent) => {
      const card = cardRef.current
      const active = document.activeElement
      const inCard = !!card && !!active && card.contains(active)

      if (e.key === 'Escape') { e.preventDefault(); actions.current.skip(); return }

      if (e.key === 'Tab') {
        // Focus stays in the card: Tab wraps, and coming back from the page lands on it.
        const items = card ? Array.from(card.querySelectorAll<HTMLElement>(FOCUSABLE)) : []
        if (!card || items.length === 0) return
        const first = items[0], end = items[items.length - 1]
        if (!inCard) { e.preventDefault(); (e.shiftKey ? end : first).focus(); return }
        if (e.shiftKey && (active === first || active === card)) { e.preventDefault(); end.focus() }
        else if (!e.shiftKey && active === end) { e.preventDefault(); first.focus() }
        return
      }

      // Someone typing in the page behind is not asking to move the tour.
      if (!inCard && active && active !== document.body) return
      if (e.key === forward || e.key === 'Enter') {
        // A focused button does its own Enter.
        if (e.key === 'Enter' && active instanceof HTMLElement && active.matches('button, a[href]')) return
        e.preventDefault()
        actions.current.next()
      } else if (e.key === backward) {
        e.preventDefault()
        actions.current.back()
      }
    }
    document.addEventListener('keydown', onKey)
    return () => document.removeEventListener('keydown', onKey)
  }, [dir])

  if (typeof document === 'undefined' || !step) return null

  // ─── Geometry for this render ───────────────────────────────────────────
  const W = geo.W || 1440, H = geo.H || 900
  const compact = W < COMPACT_WIDTH
  const hole = geo.r ? { x: geo.r.x - PAD, y: geo.r.y - PAD, w: geo.r.w + PAD * 2, h: geo.r.h + PAD * 2 } : null
  const pos = place(hole, W, H, geo.ch, compact, step.placement)
  const cut = hole ?? { x: W / 2, y: H / 2, w: 0, h: 0 }
  const shown = !!(geo.r || placed)

  const panel = (x: number, y: number, w: number, h: number): CSSProperties =>
    ({ left: x, top: y, width: Math.max(0, w), height: Math.max(0, h) })
  const line = '1px solid var(--tl)'
  const arrow: CSSProperties =
    pos.side === null ? { display: 'none' }
    : pos.side === 'top' ? { top: -7, left: (pos.off ?? 0) - 7, borderTop: line, borderLeft: line }
    : pos.side === 'bottom' ? { bottom: -7, left: (pos.off ?? 0) - 7, borderBottom: line, borderRight: line }
    : pos.side === 'right' ? { right: -7, top: (pos.off ?? 0) - 7, borderTop: line, borderRight: line }
    : { left: -7, top: (pos.off ?? 0) - 7, borderBottom: line, borderLeft: line }

  const num = (v: number) => language === 'ar' ? String(v).replace(/\d/g, (d) => '٠١٢٣٤٥٦٧٨٩'[Number(d)]) : String(v)
  const copy = copyFor(step, device)
  const nextLabel = last ? t(feature ? 'tour.got' : 'tour.start') : t('tour.next')

  return createPortal(
    <div ref={layerRef} className="tour-layer" dir={dir} data-placed={placed ? '' : undefined}>
      {/* Four panels round the hole: they blur the page and catch clicks outside the target. */}
      <div className="tour-blur" style={panel(0, 0, W, cut.y)} />
      <div className="tour-blur" style={panel(0, cut.y + cut.h, W, H - cut.y - cut.h)} />
      <div className="tour-blur" style={panel(0, cut.y, cut.x, cut.h)} />
      <div className="tour-blur" style={panel(cut.x + cut.w, cut.y, W - cut.x - cut.w, cut.h)} />
      {/* The ring, and the dim as its shadow: nothing is drawn in the hole, and it does not take clicks. */}
      <div
        className="tour-ring"
        style={{
          ...panel(cut.x, cut.y, cut.w, cut.h),
          borderRadius: hole ? 12 : 0,
          boxShadow: hole
            ? '0 0 0 2px #F59E0B, 0 0 0 6px rgba(245,158,11,.20), 0 0 0 9999px var(--dim)'
            : '0 0 0 9999px var(--dim)',
        }}
      />

      <div
        ref={cardRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        data-tour-card=""
        tabIndex={-1}
        className="tour-card"
        style={{
          left: pos.left, top: pos.top, width: pos.cw, opacity: shown ? 1 : 0,
          padding: compact ? '16px 16px 14px' : '18px 20px 16px',
        }}
      >
        <div className="tour-arrow" style={arrow} />
        <div
          className="tour-content relative flex flex-col gap-2"
          style={{ opacity: swapping ? 0 : 1, transform: swapping ? 'translateY(4px)' : 'none' }}
        >
          <div className="flex min-h-[32px] items-center gap-2">
            {feature && showNew && (
              <span className="rounded-full px-2 py-[5px] text-xs font-bold leading-none" style={{ background: 'var(--ta)', color: 'var(--ton)' }}>
                {t('tour.new')}
              </span>
            )}
            <span aria-live="polite" className="font-mono text-xs tracking-[0.04em]" style={{ color: 'var(--tat)' }}>
              {tf('tour.stepOf', { n: num(i + 1), total: num(n) })}
            </span>
            {!last && (
              <button
                type="button"
                onClick={skip}
                className="tour-skip -my-[6px] -me-1.5 ms-auto flex min-h-[44px] items-center rounded-md px-1.5 text-[13px] focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
                style={{ color: 'var(--tm)' }}
              >
                {t('tour.skip')}
              </button>
            )}
          </div>
          <h3 id={titleId} className="m-0 text-[17px] font-bold leading-[1.45] [text-wrap:balance]" style={{ color: 'var(--th)' }}>
            {t(copy.titleKey)}
          </h3>
          <p className="m-0 text-sm leading-[1.7] [text-wrap:pretty]" style={{ color: 'var(--tt)' }}>
            {t(copy.bodyKey)}
          </p>
          <div className="mt-1.5 flex items-center gap-3">
            <div aria-hidden="true" className="flex items-center gap-1">
              {steps.map((s, j) => (
                <span
                  key={j}
                  style={{
                    width: j === i ? 18 : 6, height: 6, borderRadius: 3,
                    background: j <= i ? 'var(--ta)' : 'var(--tl)',
                    transition: 'width .25s cubic-bezier(.2,.7,.2,1), background .25s',
                  }}
                />
              ))}
            </div>
            <div className="ms-auto flex gap-2">
              {i > 0 && (
                <button
                  type="button"
                  onClick={back}
                  className="tour-ghost flex min-h-[44px] items-center rounded-lg px-3.5 text-sm focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
                  style={{ border: line, color: 'var(--th)' }}
                >
                  {t('tour.back')}
                </button>
              )}
              <button
                type="button"
                onClick={next}
                className="tour-next flex min-h-[44px] items-center rounded-lg px-[18px] text-sm font-semibold focus-visible:outline focus-visible:outline-2 focus-visible:outline-ring"
                style={{ background: 'var(--ta)', color: 'var(--ton)' }}
              >
                {nextLabel}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>,
    document.body,
  )
}
