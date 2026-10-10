'use client'
import { useEffect, useRef, useSyncExternalStore } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/store'
import { authHref, currentPath, nextFromLocation } from '@/lib/authRedirect'

/**
 * For pages that need an account (a lesson, the dashboard, the mentor). A
 * signed-out visitor is sent to sign in, and brought back here afterwards
 * (`?next=` is this page). Pages anyone may browse use `useSession` instead.
 */
export function useAuth(redirectTo?: string) {
  const router = useRouter()
  const { user, token, _hasHydrated } = useAuthStore()

  useEffect(() => {
    if (!_hasHydrated) return
    if (!token) router.replace(redirectTo ?? authHref('login', currentPath()))
  }, [token, _hasHydrated, router, redirectTo])

  return { user, isAuthenticated: !!token, isLoading: !_hasHydrated }
}

/**
 * For pages anyone may browse (catalogues, course and challenge overviews,
 * plans): who is signed in, if anyone, with no redirect. A signed-out visitor
 * sees the page; reaching for something that needs an account opens the
 * sign-in prompt (see components/auth/AuthPrompt).
 */
export function useSession() {
  const { user, token, _hasHydrated } = useAuthStore()
  return { user, isAuthenticated: !!token, isLoading: !_hasHydrated }
}

const noSubscribe = () => () => {}

/**
 * The safe `?next=` this page was opened with, or null. Read after hydration
 * (the server has no address bar), so links that carry it never mismatch.
 */
export function useNextParam(): string | null {
  return useSyncExternalStore(noSubscribe, nextFromLocation, () => null)
}

/**
 * For pages only a signed-out visitor should see (sign in, sign up).
 *
 * It redirects someone who was ALREADY signed in when they arrived — and only
 * them. A visitor who signs in *on* the page is the page's own business: it knows
 * where they should go next (sign-up sends a new account to onboarding, not the
 * dashboard). Redirecting on any token change made this hook race the page's own
 * navigation and win, which sent every new account to /dashboard and past the
 * onboarding it had just been routed to.
 */
export function useGuest(redirectTo = '/dashboard') {
  const router = useRouter()
  const { token, _hasHydrated } = useAuthStore()
  // null until hydration tells us whether they arrived signed in.
  const arrivedSignedIn = useRef<boolean | null>(null)

  useEffect(() => {
    if (!_hasHydrated) return
    if (arrivedSignedIn.current === null) arrivedSignedIn.current = !!token
    if (!token) {
      arrivedSignedIn.current = false // signed out here: the next sign-in is the page's to route
      return
    }
    // Someone already signed in who followed a "sign in to continue" link goes
    // straight on to where they were headed.
    if (arrivedSignedIn.current) router.replace(nextFromLocation() ?? redirectTo)
  }, [token, _hasHydrated, router, redirectTo])
}
