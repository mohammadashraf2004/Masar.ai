'use client'
import { createContext, useCallback, useContext, useEffect, useMemo, useState } from 'react'
import { usePathname } from 'next/navigation'

/**
 * Open/closed state for the mobile navigation menu.
 *
 * It lives in context rather than in AppShell's own state because the button
 * that opens the menu (ShellHeader) and the panel it opens (MobileMenu) are
 * siblings, and either may be reached from deeper components that should not
 * be handed a setter to thread through.
 *
 * `available` is false when no AppShell wraps the tree — the exam runner
 * renders its own shell — so anything that toggles the menu can render nothing
 * instead of opening one that isn't there.
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
