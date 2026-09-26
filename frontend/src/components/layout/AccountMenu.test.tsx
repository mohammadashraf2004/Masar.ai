import { render, screen } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { AccountMenu } from '@/components/layout/AccountMenu'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import type { User } from '@/types'

const signIn = (over: Partial<User> = {}) =>
  useAuthStore.setState({
    token: 'tok', expiresAt: null, _hasHydrated: true,
    user: { full_name: 'Amira Hassan', email: 'amira@example.com', experience_level: 'beginner', role: 'student', ...over } as User,
  })

describe('AccountMenu', () => {
  beforeEach(() => signIn())

  it('has a name that is not just an initial, and says whether it is open', async () => {
    const user = userEvent.setup()
    render(<AccountMenu />)
    const trigger = screen.getByRole('button', { name: 'Profile menu: Amira Hassan' })
    expect(trigger).toHaveAttribute('type', 'button')
    expect(trigger).toHaveAttribute('aria-expanded', 'false')
    await user.click(trigger)
    expect(trigger).toHaveAttribute('aria-expanded', 'true')
    expect(screen.getByRole('link', { name: /Profile & Scorecard/ })).toBeInTheDocument()
  })

  it('closes on Escape and hands focus back to the avatar', async () => {
    const user = userEvent.setup()
    render(<AccountMenu />)
    const trigger = screen.getByRole('button', { name: /Profile menu/ })
    await user.click(trigger)
    expect(screen.getByRole('link', { name: /Profile & Scorecard/ })).toBeInTheDocument()
    await user.keyboard('{Escape}')
    expect(screen.queryByRole('link', { name: /Profile & Scorecard/ })).toBeNull()
    expect(trigger).toHaveAttribute('aria-expanded', 'false')
    expect(trigger).toHaveFocus()
  })

  it('closes when the pointer goes elsewhere', async () => {
    const user = userEvent.setup()
    render(<div><AccountMenu /><p>elsewhere</p></div>)
    await user.click(screen.getByRole('button', { name: /Profile menu/ }))
    await user.click(screen.getByText('elsewhere'))
    expect(screen.queryByRole('link', { name: /Profile & Scorecard/ })).toBeNull()
  })

  it('is named in Arabic for an Arabic reader', () => {
    useLanguageStore.setState({ language: 'ar' })
    render(<AccountMenu />)
    expect(screen.getByRole('button', { name: 'قائمة الحساب: Amira Hassan' })).toBeInTheDocument()
  })

  it('shows the initial in the avatar, hidden from assistive technology (the button carries the name)', () => {
    render(<AccountMenu />)
    const initial = screen.getByText('A')
    expect(initial).toHaveAttribute('aria-hidden', 'true')
  })

  it('offers the admin analytics link only to an admin', async () => {
    const user = userEvent.setup()
    const { unmount } = render(<AccountMenu />)
    await user.click(screen.getByRole('button', { name: /Profile menu/ }))
    expect(screen.queryByRole('link', { name: /Admin analytics/ })).toBeNull()
    unmount()

    signIn({ role: 'admin' })
    render(<AccountMenu />)
    await user.click(screen.getByRole('button', { name: /Profile menu/ }))
    expect(screen.getByRole('link', { name: /Admin analytics/ })).toHaveAttribute('href', '/admin/analytics')
  })

  it('signs out from its last row, and closes', async () => {
    const logout = vi.fn()
    useAuthStore.setState({ logout })
    const user = userEvent.setup()
    render(<AccountMenu />)
    await user.click(screen.getByRole('button', { name: /Profile menu/ }))
    await user.click(screen.getByRole('button', { name: 'Sign out' }))
    expect(logout).toHaveBeenCalledTimes(1)
    expect(screen.queryByRole('button', { name: 'Sign out' })).toBeNull()
  })

  it('renders nothing for a visitor who is not signed in', () => {
    useAuthStore.setState({ token: null, user: null })
    const { container } = render(<AccountMenu />)
    expect(container).toBeEmptyDOMElement()
  })
})
