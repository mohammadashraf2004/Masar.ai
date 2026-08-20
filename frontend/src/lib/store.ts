import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import type { User } from '@/types'
import { api } from '@/lib/api'

interface AuthState {
  user: User | null
  token: string | null
  _hasHydrated: boolean
  setAuth: (token: string, user: User) => void
  logout: () => void
  refreshUser: () => Promise<void>
  setHasHydrated: (val: boolean) => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      _hasHydrated: false,

      setHasHydrated: (val) => set({ _hasHydrated: val }),

      setAuth: (token, user) => {
        set({ token, user })
      },

      logout: () => {
        set({ token: null, user: null })
        if (typeof window !== 'undefined') {
          window.location.href = '/auth/login'
        }
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
      name: 'auth-storage',
      storage: createJSONStorage(() =>
        typeof window !== 'undefined' ? localStorage : {
          getItem: () => null,
          setItem: () => {},
          removeItem: () => {},
        }
      ),
      partialize: (s) => ({ token: s.token, user: s.user }),
      onRehydrateStorage: () => (state) => {
        state?.setHasHydrated(true)
      },
    }
  )
)
