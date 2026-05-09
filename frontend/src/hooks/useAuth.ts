'use client'
import { useEffect } from 'react'
import { useRouter } from 'next/navigation'
import { useAuthStore } from '@/lib/store'

export function useAuth(redirectTo = '/auth/login') {
  const router = useRouter()
  const { user, token } = useAuthStore()

  useEffect(() => {
    if (!token) router.replace(redirectTo)
  }, [token, router, redirectTo])

  return { user, isAuthenticated: !!token }
}

export function useGuest(redirectTo = '/dashboard') {
  const router = useRouter()
  const { token } = useAuthStore()

  useEffect(() => {
    if (token) router.replace(redirectTo)
  }, [token, router, redirectTo])
}
