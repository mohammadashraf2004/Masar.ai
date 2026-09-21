import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import LoginPage from '@/app/auth/login/page'
import { Button } from '@/components/ui/Button'
import { Input } from '@/components/ui/Input'
import { Spinner } from '@/components/ui/index'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import { setSearch } from '@/test/nav'

vi.mock('@/hooks/useAuth', () => ({ useGuest: () => {} }))
vi.mock('@/lib/api', () => ({ api: { login: vi.fn(), verifyEmail: vi.fn() } }))
import { api } from '@/lib/api'

beforeEach(() => {
  useLanguageStore.setState({ language: 'en' })
  useAuthStore.setState({ token: null, user: null, expiresAt: null, _hasHydrated: true })
  setSearch('')
})

describe('loading is announced once', () => {
  it('a bare spinner is decorative: nothing for a screen reader', () => {
    render(<Spinner />)
    expect(screen.queryByRole('status')).toBeNull()
  })

  it('a spinner that is the only sign of loading says so, once, in the reader’s language', () => {
    const { rerender } = render(<Spinner announce />)
    expect(screen.getAllByRole('status')).toHaveLength(1)
    expect(screen.getByRole('status')).toHaveTextContent('Loading…')
    useLanguageStore.setState({ language: 'ar' })
    rerender(<Spinner announce />)
    expect(screen.getByRole('status')).toHaveTextContent('جارٍ التحميل…')
  })

  it('does not announce a second time inside a region that already says it is loading', () => {
    render(
      <div role="status" aria-label="Loading…">
        <Spinner />
      </div>,
    )
    expect(screen.getAllByRole('status')).toHaveLength(1)
  })

  it('a busy button keeps its name and says it is busy, without a live region of its own', () => {
    render(<Button loading>Sign in</Button>)
    const button = screen.getByRole('button', { name: 'Sign in' })
    expect(button).toBeDisabled()
    expect(button).toHaveAttribute('aria-busy', 'true')
    expect(screen.queryByRole('status')).toBeNull()
  })

  it('an idle button is unchanged', () => {
    render(<Button>Sign in</Button>)
    const button = screen.getByRole('button', { name: 'Sign in' })
    expect(button).not.toHaveAttribute('aria-busy')
    expect(button).toBeEnabled()
  })
})

describe('field errors', () => {
  it('announce themselves and are tied to the field, so they are read on focus as well', () => {
    render(<Input label="Email" error="Enter a valid email" />)
    const field = screen.getByLabelText('Email')
    const message = screen.getByRole('alert')
    expect(message).toHaveTextContent('Enter a valid email')
    expect(field).toHaveAttribute('aria-invalid', 'true')
    expect(field).toHaveAccessibleDescription('Enter a valid email')
  })

  it('a hint is a description, not an alert', () => {
    render(<Input label="Password" hint="At least 8 characters" />)
    expect(screen.queryByRole('alert')).toBeNull()
    expect(screen.getByLabelText('Password')).toHaveAccessibleDescription('At least 8 characters')
    expect(screen.getByLabelText('Password')).not.toHaveAttribute('aria-invalid')
  })

  it('a field with neither is left alone', () => {
    render(<Input label="Name" />)
    expect(screen.getByLabelText('Name')).not.toHaveAttribute('aria-describedby')
  })
})

describe('the sign-in form', () => {
  it('announces a failed sign-in as an alert, and only one', async () => {
    vi.mocked(api.login).mockRejectedValue({ response: { data: { detail: 'Incorrect email or password' } } })
    const user = userEvent.setup()
    render(<LoginPage />)
    expect(screen.queryByRole('alert')).toBeNull()
    await user.type(screen.getByLabelText('Email'), 'amira@example.com')
    await user.type(screen.getByLabelText('Password'), 'wrong-password')
    await user.click(screen.getByRole('button', { name: /Sign in/i }))
    await waitFor(() => expect(screen.getAllByRole('alert')).toHaveLength(1))
    expect(screen.getByRole('alert')).toHaveTextContent(/incorrect email or password/i)
  })

  it('announces an invalid verification link as an alert and a good one as a status', async () => {
    setSearch('verify_token=abc')
    vi.mocked(api.verifyEmail).mockRejectedValue(new Error('nope'))
    render(<LoginPage />)
    expect(await screen.findByRole('alert')).toHaveTextContent(/invalid or expired/)
  })
})
