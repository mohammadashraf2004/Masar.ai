import { vi } from 'vitest'

/**
 * A controllable stand-in for `next/navigation`, registered for every test by
 * setup.ts. Tests reach the router through `useRouter()` and steer what a page
 * reads with `setParams` / `setSearch`.
 */
const state = vi.hoisted(() => ({
  router: {
    push: vi.fn(),
    replace: vi.fn(),
    back: vi.fn(),
    refresh: vi.fn(),
    prefetch: vi.fn(),
  },
  params: {} as Record<string, string>,
  search: new URLSearchParams(),
  pathname: '/',
}))

vi.mock('next/navigation', () => ({
  useRouter: () => state.router,
  useParams: () => state.params,
  useSearchParams: () => state.search,
  usePathname: () => state.pathname,
}))

export const router = state.router

export function setParams(params: Record<string, string>) {
  state.params = params
}

export function setPathname(pathname: string) {
  state.pathname = pathname
}

export function setSearch(query: string) {
  state.search = new URLSearchParams(query)
}

export function resetNav() {
  Object.values(state.router).forEach((fn) => fn.mockReset())
  state.params = {}
  state.search = new URLSearchParams()
  state.pathname = '/'
}
