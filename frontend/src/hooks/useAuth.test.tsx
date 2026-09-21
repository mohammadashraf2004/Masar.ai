import { renderHook } from '@testing-library/react'
import { act } from 'react'
import { beforeEach, describe, expect, it } from 'vitest'
import { useGuest } from '@/hooks/useAuth'
import { useAuthStore } from '@/lib/store'
import { router } from '@/test/nav'

// The real hook and the real store — no mocks of either. (A page test that
// mocks `useGuest` cannot see the race this guards against; a real browser run
// did: a new account was sent to /dashboard past the onboarding it had just
// been routed to.)
describe('useGuest', () => {
  beforeEach(() => {
    useAuthStore.setState({ token: null, user: null, expiresAt: null, _hasHydrated: true })
  })

  it('redirects a visitor who arrives already signed in', () => {
    useAuthStore.setState({ token: 'tok' })
    renderHook(() => useGuest())
    expect(router.replace).toHaveBeenCalledWith('/dashboard')
  })

  it('honours a different destination for that visitor', () => {
    useAuthStore.setState({ token: 'tok' })
    renderHook(() => useGuest('/learn'))
    expect(router.replace).toHaveBeenCalledWith('/learn')
  })

  it('leaves a signed-out visitor alone', () => {
    renderHook(() => useGuest())
    expect(router.replace).not.toHaveBeenCalled()
  })

  it('does not fight the page over where a visitor who signs in HERE goes next', () => {
    renderHook(() => useGuest())
    act(() => useAuthStore.setState({ token: 'tok' })) // sign-up succeeded on this page
    expect(router.replace).not.toHaveBeenCalled()
  })

  it('does nothing until the store has hydrated', () => {
    useAuthStore.setState({ token: 'tok', _hasHydrated: false })
    renderHook(() => useGuest())
    expect(router.replace).not.toHaveBeenCalled()
  })

  it('treats someone who signs out and back in on the page as a fresh sign-in', () => {
    useAuthStore.setState({ token: 'tok' })
    const { rerender } = renderHook(() => useGuest())
    router.replace.mockClear()
    act(() => useAuthStore.setState({ token: null }))
    rerender()
    act(() => useAuthStore.setState({ token: 'again' }))
    expect(router.replace).not.toHaveBeenCalled()
  })
})
