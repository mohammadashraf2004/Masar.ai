import { create } from 'zustand'
import { persist } from 'zustand/middleware'
import type { User } from '@/types'
import { api } from '@/lib/api'

interface AuthState {
  user: User | null
  token: string | null
  isLoading: boolean
  setAuth: (token: string, user: User) => void
  logout: () => void
  refreshUser: () => Promise<void>
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      isLoading: false,

      setAuth: (token, user) => {
        localStorage.setItem('token', token)
        set({ token, user })
      },

      logout: () => {
        localStorage.removeItem('token')
        set({ token: null, user: null })
        window.location.href = '/auth/login'
      },

      refreshUser: async () => {
        try {
          const user = await api.getMe()
          set({ user })
        } catch {
          get().logout()
        }
      },
    }),
    {
      name: 'auth',
      partialize: (s) => ({ token: s.token, user: s.user }),
    }
  )
)
