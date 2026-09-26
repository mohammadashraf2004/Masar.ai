import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import NotFound from '@/app/not-found'
import ErrorPage from '@/app/error'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import type { User } from '@/types'

vi.mock('@/lib/api', () => ({ api: { getWallet: vi.fn(), search: vi.fn() } }))
import { api } from '@/lib/api'

const student: User = {
  id: 1, email: 'amira@example.com', full_name: 'Amira Hassan', role: 'student', experience_level: 'beginner',
  is_verified: true, overall_readiness_score: 42, created_at: '2026-01-01T00:00:00Z',
  requires_legal_acceptance: false, pending_updates: [],
}
const signedIn = () => useAuthStore.setState({ token: 'tok', expiresAt: null, _hasHydrated: true, user: student })
const signedOut = () => useAuthStore.setState({ token: null, expiresAt: null, _hasHydrated: true, user: null })

beforeEach(() => {
  vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 100 })
  signedOut()
})
afterEach(() => vi.restoreAllMocks())

describe('the 404 page', () => {
  it('says the page is not there and offers the dashboard and the tracks', () => {
    render(<NotFound />)
    expect(screen.getByRole('heading', { level: 1, name: 'Page not found' })).toBeInTheDocument()
    expect(screen.getByText(/does not exist, or it has moved/)).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Go to dashboard' })).toHaveAttribute('href', '/dashboard')
    expect(screen.getByRole('link', { name: 'Browse tracks' })).toHaveAttribute('href', '/tracks')
  })

  it('makes the dashboard the primary action and the tracks the secondary one', () => {
    render(<NotFound />)
    expect(screen.getByRole('link', { name: 'Go to dashboard' })).toHaveClass('bg-amber')
    expect(screen.getByRole('link', { name: 'Browse tracks' })).not.toHaveClass('bg-amber')
  })

  it('shows a large mono number in the quiet colour, kept out of the reading order and always left-to-right', () => {
    render(<NotFound />)
    const code = screen.getByText('404')
    expect(code).toHaveClass('font-mono', 'text-ghost')
    expect(code).toHaveAttribute('aria-hidden', 'true')
    expect(code).toHaveAttribute('dir', 'ltr')
  })

  it('offers no "try again": a page that is not there is not there the next time either', () => {
    render(<NotFound />)
    expect(screen.queryByRole('button', { name: 'Try again' })).toBeNull()
  })

  describe('signed out', () => {
    it('is the bare page, with no app shell to offer', () => {
      render(<NotFound />)
      expect(screen.queryByRole('complementary')).toBeNull()
      expect(screen.queryByRole('navigation', { name: 'Menu' })).toBeNull()
    })

    it('is also what a first render shows, before the saved session has been read', () => {
      useAuthStore.setState({ token: 'tok', user: student, _hasHydrated: false })
      render(<NotFound />)
      expect(screen.queryByRole('complementary')).toBeNull()
    })
  })

  describe('signed in', () => {
    it('sits inside the app shell, so the sidebar is still there to leave by', () => {
      signedIn()
      render(<NotFound />)
      const sidebar = screen.getByRole('complementary')
      expect(within(sidebar).getByRole('link', { name: 'Dashboard' })).toBeInTheDocument()
      expect(screen.getByRole('heading', { level: 1, name: 'Page not found' })).toBeInTheDocument()
    })
  })

  it('reads in Arabic for an Arabic reader', () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<NotFound />)
    expect(screen.getByRole('heading', { level: 1, name: 'الصفحة غير موجودة' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'إلى لوحة التحكم' })).toHaveAttribute('href', '/dashboard')
    expect(screen.getByRole('link', { name: 'تصفّح المسارات' })).toHaveAttribute('href', '/tracks')
    expect(screen.queryByText('Page not found')).toBeNull()
  })
})

describe('the error page', () => {
  const boom = Object.assign(new Error('boom'), { digest: 'abc123' })

  it('says something went wrong, with the same two exits as the 404 page', () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    render(<ErrorPage error={boom} reset={() => {}} />)
    expect(screen.getByText('500')).toHaveAttribute('aria-hidden', 'true')
    expect(screen.getByRole('heading', { level: 1, name: 'Something went wrong' })).toBeInTheDocument()
    expect(screen.getByRole('link', { name: 'Go to dashboard' })).toHaveAttribute('href', '/dashboard')
    expect(screen.getByRole('link', { name: 'Browse tracks' })).toHaveAttribute('href', '/tracks')
  })

  it('offers to try again, which asks the framework to re-render the page', async () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    const reset = vi.fn()
    render(<ErrorPage error={boom} reset={reset} />)
    await userEvent.setup().click(screen.getByRole('button', { name: 'Try again' }))
    expect(reset).toHaveBeenCalledTimes(1)
  })

  it('logs the failure, so it is not swallowed', () => {
    const log = vi.spyOn(console, 'error').mockImplementation(() => {})
    render(<ErrorPage error={boom} reset={() => {}} />)
    expect(log).toHaveBeenCalledWith(boom)
  })

  it('sits inside the app shell when signed in, and reads in Arabic for an Arabic reader', () => {
    vi.spyOn(console, 'error').mockImplementation(() => {})
    signedIn()
    useLanguageStore.setState({ language: 'ar' })
    render(<ErrorPage error={boom} reset={() => {}} />)
    expect(screen.getByRole('complementary')).toBeInTheDocument()
    expect(screen.getByRole('heading', { level: 1, name: 'حدث خطأ ما' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'حاول مرة أخرى' })).toBeInTheDocument()
  })
})
