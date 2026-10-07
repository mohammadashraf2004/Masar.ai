'use client'
import { createContext, useCallback, useContext, useEffect, useMemo, useRef, useState } from 'react'
import { usePathname, useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/store'
import { blockedRoute, modalOpen, pickTour, showsNewTag } from './eligibility'
import { ReplayBar } from './ReplayBar'
import { type TourStatus } from './records'
import { TOURS, homeRoute, routeMatches, tourById, type Device, type TourDef, type TourId, type TourStep } from './registry'
import { MIN_STEPS, resolveSteps } from './targets'
import { clearPendingReplay, markTourSession, peekPendingReplay, setPendingReplay, toursEnabled, tourRanThisSession } from './session'
import { ensureSynced, saveAndSync } from './sync'
import { Tour } from './Tour'

/**
 * Decides when a walkthrough runs, runs it, and remembers what came of it.
 *
 * It sits in the app shell, so it exists on every signed-in page but on none of the sign-in,
 * payment or exam pages, and it starts nothing over a dialog. A tour starts once the page
 * has had a moment to put its targets on screen; a step whose target never shows up is left
 * out, and a tour left with fewer than two steps does not run at all.
 */

/** Below the `lg` breakpoint the sidebar is gone, so a step points at its on-page equivalent. */
const DESKTOP_MIN_WIDTH = 1024
/** How often to look again for targets, or for a dialog to close. */
const RETRY_MS = 400
/** How long the page gets to show its targets before the tour goes ahead with those it has. */
const SETTLE_MS = 3000
/** How long to wait for a dialog to close before giving up until the next visit. */
const MAX_BLOCKED_MS = 120_000

function currentDevice(): Device {
  return window.innerWidth >= DESKTOP_MIN_WIDTH ? 'desktop' : 'mobile'
}

function useDevice(): Device {
  const [device, setDevice] = useState<Device>('desktop')
  useEffect(() => {
    const update = () => setDevice(currentDevice())
    update()
    window.addEventListener('resize', update)
    return () => window.removeEventListener('resize', update)
  }, [])
  return device
}

interface Run {
  tour: TourDef
  steps: TourStep[]
  showNew: boolean
  replay: boolean
}

interface TourApi {
  /** Play a tour again: the given one, else the one for this page, else the first-run tour. */
  replay: (id?: TourId) => void
}

const TourContext = createContext<TourApi | null>(null)

/** The Help menu's way in. `null` outside the app shell, where there is nothing to replay. */
export function useTours(): TourApi | null {
  return useContext(TourContext)
}

export function TourProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()
  const router = useRouter()
  const user = useAuthStore((s) => s.user)
  const device = useDevice()
  const [run, setRun] = useState<Run | null>(null)
  // The tour that just ended, for the "replay" note.
  const [ended, setEnded] = useState<TourId | null>(null)
  const stop = useRef<(() => void) | null>(null)

  const userId = user?.id
  const latest = useRef({ user, run })
  useEffect(() => { latest.current = { user, run } })

  // Pull the account's tour records onto this browser, and push up anything only it has —
  // fire-and-forget, so it never delays a tour that is already due locally. See sync.ts.
  useEffect(() => {
    if (!userId || !toursEnabled()) return
    void ensureSynced(userId)
  }, [userId])

  /** Wait for the page to be ready, then start `tour`. Returns how to cancel. */
  const launch = useCallback((tour: TourDef, replay: boolean, pathname: string): (() => void) => {
    let timer: ReturnType<typeof setTimeout> | undefined
    let cancelled = false
    const began = Date.now()
    let settling: number | null = null

    const tick = () => {
      if (cancelled) return
      const account = latest.current.user
      if (!account || (!replay && tourRanThisSession())) return
      if (blockedRoute(pathname) || modalOpen()) {
        settling = null
        if (Date.now() - began < MAX_BLOCKED_MS) timer = setTimeout(tick, RETRY_MS)
        return
      }
      settling ??= Date.now()
      const steps = resolveSteps(tour, currentDevice())
      if (steps.length === tour.steps.length || Date.now() - settling >= SETTLE_MS) {
        // Too few of its targets are here to be worth it: not run, and not recorded.
        if (steps.length < MIN_STEPS) return
        markTourSession()
        if (replay) clearPendingReplay()
        setEnded(null)
        setRun({ tour, steps, showNew: showsNewTag(tour, account), replay })
        return
      }
      timer = setTimeout(tick, RETRY_MS)
    }
    tick()
    return () => { cancelled = true; clearTimeout(timer) }
  }, [])

  const begin = useCallback((tour: TourDef, replay: boolean, at: string) => {
    stop.current?.()
    stop.current = launch(tour, replay, at)
  }, [launch])

  // A tour starts when its page opens, if it is due.
  useEffect(() => {
    const { user: account, run: running } = latest.current
    if (!toursEnabled() || !account || running) return

    const pending = peekPendingReplay()
    const wanted = TOURS.find((t) => t.id === pending)
    if (wanted && routeMatches(wanted, pathname)) {
      begin(wanted, true, pathname)
    } else {
      // A replay for a page we did not land on (a redirect) is dropped, not carried around.
      if (wanted) clearPendingReplay()
      const due = pickTour(pathname, account, tourRanThisSession())
      if (due) begin(due, false, pathname)
    }
    return () => { stop.current?.(); stop.current = null }
  }, [pathname, userId, begin])

  const finish = useCallback((status: TourStatus) => {
    const { user: account, run: running } = latest.current
    if (!running) return
    // A replay changes nothing: it must not turn a finished tour into a skipped one.
    if (!running.replay && account) {
      saveAndSync(account.id, running.tour.id, { status, version: running.tour.version })
    }
    setRun(null)
    setEnded(running.tour.id)
  }, [])

  const replay = useCallback((id?: TourId) => {
    const tour = id ? tourById(id) : (TOURS.find((t) => routeMatches(t, pathname)) ?? tourById('onboarding'))
    if (routeMatches(tour, pathname)) {
      setRun(null)
      begin(tour, true, pathname)
    } else {
      // Its targets are on another page: go there, and it starts when it arrives.
      setPendingReplay(tour.id)
      router.push(homeRoute(tour))
    }
  }, [pathname, begin, router])

  const api = useMemo<TourApi>(() => ({ replay }), [replay])

  return (
    <TourContext.Provider value={api}>
      {children}
      {run && <Tour key={run.tour.id} tour={run.tour} steps={run.steps} device={device} showNew={run.showNew} onFinish={finish} />}
      {ended && !run && (
        <ReplayBar
          onDismiss={() => setEnded(null)}
          onReplay={() => { const id = ended; setEnded(null); replay(id) }}
        />
      )}
    </TourContext.Provider>
  )
}
