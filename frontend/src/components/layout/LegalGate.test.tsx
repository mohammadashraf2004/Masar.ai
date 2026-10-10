import { act, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { LegalGate } from '@/components/layout/LegalGate'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import type { LegalDocument, User } from '@/types'

vi.mock('@/lib/api', () => ({ api: { acceptLegal: vi.fn(), getMe: vi.fn(), getLegalDocument: vi.fn() } }))
import { api } from '@/lib/api'

const user = (over: Partial<User> = {}) =>
  ({ id: 1, email: 'a@example.com', full_name: 'A', ...over }) as User

function signIn(u: User) {
  useAuthStore.setState({ token: 'tok', user: u, expiresAt: null, _hasHydrated: true, logout: vi.fn() })
}

beforeEach(() => {
  useAuthStore.setState({ token: null, user: null, expiresAt: null, _hasHydrated: true })
  vi.mocked(api.acceptLegal).mockResolvedValue(user({ requires_legal_acceptance: false, terms_version: '2026-09-01' }))
  vi.mocked(api.getMe).mockResolvedValue(user({ requires_legal_acceptance: false }))
  vi.mocked(api.getLegalDocument).mockImplementation(async (kind) => doc(kind as 'terms' | 'privacy'))
})

const doc = (kind: 'terms' | 'privacy'): LegalDocument => ({
  kind,
  version: '2026-09-01',
  language: 'en',
  title: kind === 'terms' ? 'Terms of Service' : 'Privacy Policy',
  intro: `The ${kind} intro.`,
  sections: [{ heading: `1. ${kind} first section`, body: [`A ${kind} paragraph.`] }],
})

describe('re-acceptance of the Terms and Privacy Policy', () => {
  it('asks an account that has not accepted the current versions', () => {
    signIn(user({ requires_legal_acceptance: true }))
    render(<LegalGate />)
    const dialog = screen.getByRole('dialog', { name: 'We updated our Terms and Privacy Policy' })
    expect(dialog).toHaveAttribute('aria-modal', 'true')
    expect(screen.getByText('Please review and accept them to keep using Masar.')).toBeInTheDocument()
  })

  it('says nothing to an account that is up to date', () => {
    signIn(user({ requires_legal_acceptance: false }))
    const { container } = render(<LegalGate />)
    expect(container).toBeEmptyDOMElement()
  })

  it('says nothing to a signed-out visitor', () => {
    const { container } = render(<LegalGate />)
    expect(container).toBeEmptyDOMElement()
  })

  it('does not decide anything from version strings — only the server\'s flag counts', () => {
    signIn(user({ requires_legal_acceptance: false, terms_version: '1999-01-01', privacy_version: null }))
    const { container } = render(<LegalGate />)
    expect(container).toBeEmptyDOMElement()
  })

  it('has an unchecked checkbox, real links to the documents, and a disabled button until ticked', async () => {
    const u = userEvent.setup()
    signIn(user({ requires_legal_acceptance: true }))
    render(<LegalGate />)
    const box = screen.getByRole('checkbox', { name: /I agree to the/ })
    expect(box).not.toBeChecked()
    expect(screen.getByRole('link', { name: 'Terms of Service' })).toHaveAttribute('href', '/terms')
    expect(screen.getByRole('link', { name: 'Privacy Policy' })).toHaveAttribute('href', '/privacy')
    const accept = screen.getByRole('button', { name: 'Accept and continue' })
    expect(accept).toBeDisabled()
    await u.click(box)
    expect(accept).toBeEnabled()
  })

  // In-app browsers (WhatsApp, Facebook, Instagram) ignore target="_blank", so a
  // new-tab link did nothing there: the documents must open inside the dialog.
  it('opens the Terms inside the dialog, and Back returns with the tick kept', async () => {
    const u = userEvent.setup()
    signIn(user({ requires_legal_acceptance: true }))
    render(<LegalGate />)
    await u.click(screen.getByRole('checkbox'))
    const link = screen.getByRole('link', { name: 'Terms of Service' })
    expect(link).not.toHaveAttribute('target')
    await u.click(link)

    const dialog = await screen.findByRole('dialog', { name: 'Terms of Service' })
    expect(api.getLegalDocument).toHaveBeenCalledWith('terms', 'en')
    expect(dialog).toHaveTextContent('A terms paragraph.')
    expect(dialog).toHaveTextContent('Version 2026-09-01')
    const back = screen.getByRole('button', { name: 'Back' })
    expect(back).toHaveFocus()

    await u.click(back)
    expect(screen.getByRole('dialog', { name: 'We updated our Terms and Privacy Policy' })).toBeInTheDocument()
    expect(screen.getByRole('checkbox')).toBeChecked()
    expect(screen.getByRole('link', { name: 'Terms of Service' })).toHaveFocus()
  })

  it('opens the Privacy Policy inside the dialog without ticking the box', async () => {
    const u = userEvent.setup()
    signIn(user({ requires_legal_acceptance: true }))
    render(<LegalGate />)
    await u.click(screen.getByRole('link', { name: 'Privacy Policy' }))
    expect(await screen.findByRole('dialog', { name: 'Privacy Policy' })).toHaveTextContent('A privacy paragraph.')
    await u.click(screen.getByRole('button', { name: 'Back' }))
    expect(screen.getByRole('checkbox')).not.toBeChecked()
  })

  it('leaves a Ctrl/Cmd click to the browser (new tab to the public page)', () => {
    signIn(user({ requires_legal_acceptance: true }))
    render(<LegalGate />)
    const link = screen.getByRole('link', { name: 'Terms of Service' })
    const event = new MouseEvent('click', { bubbles: true, cancelable: true, ctrlKey: true, button: 0 })
    act(() => { link.dispatchEvent(event) })
    expect(event.defaultPrevented).toBe(false)
    expect(api.getLegalDocument).not.toHaveBeenCalled()
  })

  it('says so when a document cannot be loaded, and retries', async () => {
    const u = userEvent.setup()
    vi.mocked(api.getLegalDocument).mockRejectedValueOnce(new Error('down'))
    signIn(user({ requires_legal_acceptance: true }))
    render(<LegalGate />)
    await u.click(screen.getByRole('link', { name: 'Terms of Service' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load this document.')
    await u.click(screen.getByRole('button', { name: 'Try again' }))
    expect(await screen.findByRole('dialog', { name: 'Terms of Service' })).toHaveTextContent('A terms paragraph.')
  })

  it('records the agreement with the server and then gets out of the way', async () => {
    const u = userEvent.setup()
    signIn(user({ requires_legal_acceptance: true }))
    render(<LegalGate />)
    await u.click(screen.getByRole('checkbox'))
    await u.click(screen.getByRole('button', { name: 'Accept and continue' }))
    await waitFor(() => expect(screen.queryByRole('dialog')).toBeNull())
    expect(api.acceptLegal).toHaveBeenCalledWith() // no version, no body of its own
    expect(useAuthStore.getState().user?.requires_legal_acceptance).toBe(false)
  })

  it('reports a failure, stays open, and lets them try again', async () => {
    const u = userEvent.setup()
    vi.mocked(api.acceptLegal).mockRejectedValueOnce(new Error('down'))
    signIn(user({ requires_legal_acceptance: true }))
    render(<LegalGate />)
    await u.click(screen.getByRole('checkbox'))
    await u.click(screen.getByRole('button', { name: 'Accept and continue' }))
    expect(await screen.findByRole('alert')).toHaveTextContent('We could not record your acceptance.')
    expect(screen.getByRole('dialog')).toBeInTheDocument()
    await u.click(screen.getByRole('button', { name: 'Accept and continue' }))
    await waitFor(() => expect(screen.queryByRole('dialog')).toBeNull())
  })

  it('does not trap the learner: they can still sign out', async () => {
    const u = userEvent.setup()
    const logout = vi.fn()
    useAuthStore.setState({ token: 'tok', user: user({ requires_legal_acceptance: true }), _hasHydrated: true, logout })
    render(<LegalGate />)
    await u.click(screen.getByRole('button', { name: 'Sign out' }))
    expect(logout).toHaveBeenCalled()
  })

  it('refreshes a session that predates the feature, once, and prompts if the server says so', async () => {
    vi.mocked(api.getMe).mockResolvedValue(user({ requires_legal_acceptance: true }))
    signIn(user()) // a stored user with no such field
    render(<LegalGate />)
    expect(await screen.findByRole('dialog')).toBeInTheDocument()
    expect(api.getMe).toHaveBeenCalledTimes(1)
  })

  it('does not mark anyone as accepted when the account cannot be read', async () => {
    vi.mocked(api.getMe).mockRejectedValue(new Error('down'))
    signIn(user())
    const { container } = render(<LegalGate />)
    await act(async () => { await new Promise((r) => setTimeout(r, 0)) })
    expect(container).toBeEmptyDOMElement()
    expect(api.acceptLegal).not.toHaveBeenCalled()
  })

  it('does not refetch when the account already carries the flag', () => {
    signIn(user({ requires_legal_acceptance: false }))
    render(<LegalGate />)
    expect(api.getMe).not.toHaveBeenCalled()
  })

  it('is written in Arabic for an Arabic reader', () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    signIn(user({ requires_legal_acceptance: true }))
    render(<LegalGate />)
    expect(screen.getByRole('dialog', { name: 'حدّثنا شروط الخدمة وسياسة الخصوصية' })).toBeInTheDocument()
    expect(screen.getByRole('button', { name: 'أوافق وأتابع' })).toBeDisabled()
  })
})
