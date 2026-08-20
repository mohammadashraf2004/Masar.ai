'use client'
import { useEffect } from 'react'
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

export function useGuest(redirectTo = '/dashboard') {
  const router = useRouter()
  const { token, _hasHydrated } = useAuthStore()

  useEffect(() => {
    if (!_hasHydrated) return
    if (token) router.replace(redirectTo)
  }, [token, _hasHydrated, router, redirectTo])
}
