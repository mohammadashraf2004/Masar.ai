'use client'
import { useEffect, useRef } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/store'

export function useAuth(redirectTo = '/auth/login') {
  const router = useRouter()
  const { user, token, _hasHydrated } = useAuthStore()

  useEffect(() => {
    if (!_hasHydrated) return
    if (!token) router.replace(redirectTo)
  }, [token, _hasHydrated, router, redirectTo])

  return { user, isAuthenticated: !!token, isLoading: !_hasHydrated }
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
    if (arrivedSignedIn.current) router.replace(redirectTo)
  }, [token, _hasHydrated, router, redirectTo])
}
