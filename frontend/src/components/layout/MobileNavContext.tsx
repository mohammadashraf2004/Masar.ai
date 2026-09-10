'use client'
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { usePathname } from 'next/navigation'

/**
 * Open/closed state for the mobile navigation drawer.
 *
 * It lives in context rather than in AppShell's own state because the control
 * that opens the drawer sits in PageHeader, which is a sibling of the sidebar
 * rather than a child of it. Passing the setter down through every page would
 * mean touching all eleven of them; this keeps the drawer a shell concern.
 *
 * `available` is false when no AppShell wraps the tree — the exam runner
 * renders its own shell — so the toggle can render nothing instead of opening
 * a drawer that isn't there.
 */
interface MobileNavState {
  open: boolean
  setOpen: (open: boolean) => void
  available: boolean
}

const MobileNavContext = createContext<MobileNavState>({
  open: false,
  setOpen: () => {},
  available: false,
})

export function MobileNavProvider({ children }: { children: React.ReactNode }) {
  const pathname = usePathname()

  // What is stored is the route the drawer was opened on, not a boolean, so
  // "closed" falls out of a route change instead of needing an effect to
  // force it. A drawer that survived navigation would cover the page the
  // reader just asked for, and resetting it in an effect would render it open
  // for one frame on the new route first.
  const [openedOn, setOpenedOn] = useState<string | null>(null)
  const open = openedOn !== null && openedOn === pathname

  const setOpen = useCallback(
    (next: boolean) => setOpenedOn(next ? pathname : null),
    [pathname],
  )

  useEffect(() => {
    if (!open) return
    const onKey = (e: KeyboardEvent) => { if (e.key === 'Escape') setOpen(false) }
    document.addEventListener('keydown', onKey)
    // Without this the page behind the drawer scrolls under it on touch.
    const previous = document.body.style.overflow
    document.body.style.overflow = 'hidden'
    return () => {
      document.removeEventListener('keydown', onKey)
      document.body.style.overflow = previous
    }
  }, [open, setOpen])

  const value = useMemo(() => ({ open, setOpen, available: true }), [open, setOpen])

  return <MobileNavContext.Provider value={value}>{children}</MobileNavContext.Provider>
}

export function useMobileNav() {
  return useContext(MobileNavContext)
}
