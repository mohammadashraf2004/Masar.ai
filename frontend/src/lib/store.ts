import { create } from 'zustand'
import { persist, createJSONStorage } from 'zustand/middleware'
import type { User } from '@/types'
import { api } from '@/lib/api'

/**
 * Token storage — a deliberate, documented trade-off.
 *
 * This is a static SPA talking to a separate cross-origin API with
 * `Authorization: Bearer`, so an HttpOnly cookie would need the API to
 * set a cross-site cookie (SameSite=None; Secure), a shared parent
 * domain, and CSRF tokens on every mutating route. That is the better
 * end state and is written up in SECURITY.md; until then the token lives
 * in localStorage, which is readable by any script running on this
 * origin — i.e. an XSS is an account takeover.
 *
 * What bounds that risk today:
 *   - the token's lifetime is 12h, not the 7 days it used to be;
 *   - a strict CSP (next.config.js) and no dangerouslySetInnerHTML on
 *     user-supplied content;
 *   - the API rejects javascript:/data: URLs on every user-writable
 *     field, so a stored payload can't be planted in the first place;
 *   - `expiresAt` below means an expired token is dropped locally rather
 *     than sitting in storage waiting to be exfiltrated.
 */
interface AuthState {
  user: User | null
  token: string | null
  expiresAt: number | null
  _hasHydrated: boolean
  setAuth: (token: string, user: User, expiresIn?: number) => void
  clearAuth: () => void
  logout: () => void
  refreshUser: () => Promise<void>
  setHasHydrated: (val: boolean) => void
  isTokenExpired: () => boolean
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set, get) => ({
      user: null,
      token: null,
      expiresAt: null,
      _hasHydrated: false,

      setHasHydrated: (val) => set({ _hasHydrated: val }),

      setAuth: (token, user, expiresIn) => {
        // expires_in comes from the API (ACCESS_TOKEN_EXPIRE_MINUTES), so
        // the client never has to parse the JWT to know when to stop
        // using it. Falls back to 12h to match the server default.
        const ttl = (expiresIn ?? 12 * 60 * 60) * 1000
        set({ token, user, expiresAt: Date.now() + ttl })
      },

      isTokenExpired: () => {
        const { expiresAt } = get()
        return expiresAt !== null && Date.now() >= expiresAt
      },

      // Drop the session without navigating. Split out of `logout` so the
      // API client can use it when it discovers a dead token mid-flight
      // (lib/api.ts) — that path has its own redirect rules and must not
      // inherit this one, but it does need both halves cleared. Clearing
      // only localStorage, as it used to, left this store still holding
      // the token and user: the UI stayed "logged in", and persist wrote
      // the stale entry straight back on the next set().
      clearAuth: () => {
        // Order matters. `set` runs the persist middleware, which writes
        // the (now null) state to localStorage; removing the key
        // afterwards is what actually leaves storage empty.
        set({ token: null, user: null, expiresAt: null })
        if (typeof window !== 'undefined') {
          try {
            localStorage.removeItem('auth-storage')
          } catch {}
        }
      },

      logout: () => {
        // Clear in-memory state AND the persisted copy — leaving a stale
        // token in localStorage after a logout is exactly the artefact an
        // XSS or a shared machine picks up later.
        get().clearAuth()
        // Already on an auth screen means there is nowhere to send them:
        // navigating again would reload the login page under itself, and
        // refreshUser() calls logout() on failure, so that reload can
        // repeat. Guarded the same way lib/api.ts guards its 401 redirect.
        if (typeof window !== 'undefined' && !window.location.pathname.startsWith('/auth/')) {
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
      partialize: (s) => ({ token: s.token, user: s.user, expiresAt: s.expiresAt }),
      onRehydrateStorage: () => (state) => {
        // Drop an already-expired token at startup instead of sending it
        // and waiting for the 401.
        if (state?.expiresAt && Date.now() >= state.expiresAt) {
          state.token = null
          state.user = null
          state.expiresAt = null
          try {
            localStorage.removeItem('auth-storage')
          } catch {}
        }
        state?.setHasHydrated(true)
      },
    }
  )
)
