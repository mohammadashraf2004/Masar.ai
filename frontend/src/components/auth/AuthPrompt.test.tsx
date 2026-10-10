import { act, fireEvent, render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it } from 'vitest'
import { AuthPromptDialog, GatedLink, useAuthPrompt, useRequireAuth } from '@/components/auth/AuthPrompt'
import { useAuthStore } from '@/lib/store'

function Harness({ next }: { next?: string }) {
  const requireAuth = useRequireAuth()
  return (
    <>
      <button type="button" onClick={() => { (window as unknown as { result: boolean }).result = requireAuth(next) }}>act</button>
      <GatedLink href="/courses/course-007/lessons/3">a lesson</GatedLink>
      <GatedLink href="/courses/course-007">the overview</GatedLink>
      <AuthPromptDialog />
    </>
  )
}

const result = () => (window as unknown as { result: boolean }).result

beforeEach(() => {
  useAuthStore.setState({ token: null, user: null, expiresAt: null, _hasHydrated: true })
  useAuthPrompt.setState({ open: false, next: null })
})

describe('requireAuth', () => {
  it('signed out: opens the dialog with Sign in and Create free account, both returning to `next`', async () => {
    const u = userEvent.setup()
    render(<Harness next="/challenges?challenge=x" />)
    expect(screen.queryByRole('dialog')).toBeNull()
    await u.click(screen.getByRole('button', { name: 'act' }))
    expect(result()).toBe(false)
    const dialog = screen.getByRole('dialog', { name: 'Sign in to continue learning' })
    expect(within(dialog).getByRole('link', { name: 'Sign in' })).toHaveAttribute('href', '/auth/login?next=%2Fchallenges%3Fchallenge%3Dx')
    expect(within(dialog).getByRole('link', { name: 'Create free account' })).toHaveAttribute('href', '/auth/register?next=%2Fchallenges%3Fchallenge%3Dx')
    // Sign in is focused: it is the primary action.
    expect(within(dialog).getByRole('link', { name: 'Sign in' })).toHaveFocus()
  })

  it('can be dismissed, and is not shown again until the next deliberate action', async () => {
    const u = userEvent.setup()
    render(<Harness />)
    await u.click(screen.getByRole('button', { name: 'act' }))
    await u.click(screen.getByRole('button', { name: 'Close' }))
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  it('an unsafe destination is dropped, not followed', async () => {
    const u = userEvent.setup()
    render(<Harness next="//evil.example" />)
    await u.click(screen.getByRole('button', { name: 'act' }))
    expect(screen.getByRole('link', { name: 'Sign in' })).toHaveAttribute('href', '/auth/login')
  })

  it('signed in: says yes and shows nothing', async () => {
    useAuthStore.setState({ token: 'tok' })
    const u = userEvent.setup()
    render(<Harness />)
    await u.click(screen.getByRole('button', { name: 'act' }))
    expect(result()).toBe(true)
    expect(screen.queryByRole('dialog')).toBeNull()
  })
})

describe('GatedLink', () => {
  it('signed out, a link to a lesson opens the dialog instead of navigating', () => {
    render(<Harness />)
    const event = new MouseEvent('click', { bubbles: true, cancelable: true, button: 0 })
    act(() => { screen.getByRole('link', { name: 'a lesson' }).dispatchEvent(event) })
    expect(event.defaultPrevented).toBe(true)
    expect(screen.getByRole('link', { name: 'Sign in' })).toHaveAttribute('href', '/auth/login?next=%2Fcourses%2Fcourse-007%2Flessons%2F3')
  })

  it('signed out, a link to a public page is an ordinary link (no popup while browsing)', () => {
    render(<Harness />)
    fireEvent.click(screen.getByRole('link', { name: 'the overview' }))
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  it('a Ctrl/Cmd click is left to the browser', () => {
    render(<Harness />)
    const event = new MouseEvent('click', { bubbles: true, cancelable: true, button: 0, ctrlKey: true })
    act(() => { screen.getByRole('link', { name: 'a lesson' }).dispatchEvent(event) })
    expect(screen.queryByRole('dialog')).toBeNull()
  })

  it('signed in, it is an ordinary link', () => {
    useAuthStore.setState({ token: 'tok' })
    render(<Harness />)
    fireEvent.click(screen.getByRole('link', { name: 'a lesson' }))
    expect(screen.queryByRole('dialog')).toBeNull()
  })
})
