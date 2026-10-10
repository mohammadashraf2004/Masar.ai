import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest'
import LoginPage from '@/app/auth/login/page'
import { useAuthStore } from '@/lib/store'

const replace = vi.fn()
vi.mock('next/navigation', () => ({
  useRouter: () => ({ replace, push: vi.fn() }),
  useSearchParams: () => new URLSearchParams(window.location.search),
  usePathname: () => '/auth/login',
}))
vi.mock('@/lib/api', () => ({ api: { login: vi.fn(), verifyEmail: vi.fn() } }))
import { api } from '@/lib/api'

beforeEach(() => {
  replace.mockReset()
  useAuthStore.setState({ token: null, user: null, expiresAt: null, _hasHydrated: true })
  vi.mocked(api.login).mockResolvedValue({
    access_token: 'tok', token_type: 'bearer', expires_in: 3600,
    user: { id: 1, email: 'a@example.com', full_name: 'A' },
  } as never)
})
afterEach(() => window.history.replaceState({}, '', '/'))

async function signIn() {
  const u = userEvent.setup()
  render(<LoginPage />)
  await u.type(screen.getByLabelText(/email/i), 'a@example.com')
  await u.type(screen.getByLabelText(/password/i), 'correct-horse-battery-staple-7')
  await u.click(screen.getByRole('button', { name: /sign in/i }))
}

describe('signing in from "sign in to continue"', () => {
  it('returns to where the visitor was headed', async () => {
    window.history.replaceState({}, '', '/auth/login?next=%2Fcourses%2Fcourse-007%2Flessons%2F702')
    await signIn()
    expect(replace).toHaveBeenCalledWith('/courses/course-007/lessons/702')
  })

  it('goes to the dashboard without a destination', async () => {
    window.history.replaceState({}, '', '/auth/login')
    await signIn()
    expect(replace).toHaveBeenCalledWith('/dashboard')
  })

  it.each(['https://evil.example/', '//evil.example/x', '/\\evil.example', '/auth/register'])(
    'never follows an unsafe destination (%s)',
    async (next) => {
      window.history.replaceState({}, '', `/auth/login?next=${encodeURIComponent(next)}`)
      await signIn()
      expect(replace).toHaveBeenCalledWith('/dashboard')
    },
  )

  it('keeps the destination on the way to creating an account', () => {
    window.history.replaceState({}, '', '/auth/login?next=%2Fchallenges')
    render(<LoginPage />)
    expect(screen.getByRole('link', { name: /create one|create an account|sign up/i }))
      .toHaveAttribute('href', '/auth/register?next=%2Fchallenges')
  })
})
