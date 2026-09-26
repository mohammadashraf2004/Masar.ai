import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import RegisterPage from '@/app/auth/register/page'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import { router } from '@/test/nav'
import type { User } from '@/types'

vi.mock('@/hooks/useAuth', () => ({ useGuest: () => {} }))
vi.mock('@/lib/api', () => ({ api: { register: vi.fn() } }))
import { api } from '@/lib/api'

beforeEach(() => {
  useAuthStore.setState({ token: null, user: null, expiresAt: null, _hasHydrated: true })
  vi.mocked(api.register).mockResolvedValue({
    access_token: 'tok', token_type: 'bearer', expires_in: 3600,
    user: { id: 7, email: 'amira@example.com', full_name: 'Amira Hassan' } as User,
  })
})

const box = () => screen.getByRole('checkbox', { name: /I agree to the/ })
const create = () => screen.getByRole('button', { name: /Create account/ })

async function fill(user: ReturnType<typeof userEvent.setup>) {
  await user.type(screen.getByLabelText('Full name'), 'Amira Hassan')
  await user.type(screen.getByLabelText('Email'), 'amira@example.com')
  await user.type(screen.getByLabelText('Password'), 'correcthorsebattery')
}

describe('the Terms and Privacy acknowledgement', () => {
  it('is a real checkbox, unchecked by default, with a label', () => {
    render(<RegisterPage />)
    expect(box()).toBeInTheDocument()
    expect(box()).not.toBeChecked()
    expect(box().tagName).toBe('INPUT')
    expect(box()).toHaveAccessibleName(/^I agree to the Terms of Service and Privacy Policy ?\.$/)
  })

  it('links "Terms of Service" and "Privacy Policy" to the actual documents, in a new tab', () => {
    render(<RegisterPage />)
    const terms = screen.getByRole('link', { name: 'Terms of Service' })
    const privacy = screen.getByRole('link', { name: 'Privacy Policy' })
    expect(terms).toHaveAttribute('href', '/terms')
    expect(privacy).toHaveAttribute('href', '/privacy')
    for (const link of [terms, privacy]) {
      expect(link).toHaveAttribute('target', '_blank')
      expect(link.getAttribute('rel')).toContain('noopener')
    }
  })

  it('does not allow creating the account until it is ticked', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)
    await fill(user)
    expect(create()).toBeDisabled()
    // The checkbox is the reason, and it says so: it is marked required for assistive technology.
    expect(box()).toBeRequired()
    await user.click(create())
    expect(api.register).not.toHaveBeenCalled()
  })

  it('states the agreement once: the label, not a second sentence under it', () => {
    render(<RegisterPage />)
    expect(screen.queryByText('Accept the Terms of Service and Privacy Policy to create your account.')).toBeNull()
    expect(box()).not.toHaveAccessibleDescription()
    expect(document.querySelectorAll('form p')).toHaveLength(0)
  })

  it('enables the button once ticked, and disables it again when unticked', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)
    await user.click(box())
    expect(create()).toBeEnabled()
    expect(screen.queryByText(/Accept the Terms of Service and Privacy Policy to create/)).toBeNull()
    await user.click(box())
    expect(create()).toBeDisabled()
  })

  it('can be ticked from its label as well as the box', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)
    await user.click(screen.getByText(/I agree to the/))
    expect(box()).toBeChecked()
  })

  it('sends only the agreement — never a version — and moves on to onboarding', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)
    await fill(user)
    await user.click(box())
    await user.click(create())
    await waitFor(() => expect(router.replace).toHaveBeenCalledWith('/onboarding/quick'))
    const sent = vi.mocked(api.register).mock.calls[0][0]
    expect(sent).toEqual({
      full_name: 'Amira Hassan', email: 'amira@example.com', password: 'correcthorsebattery',
      accept_terms: true, accept_privacy: true,
    })
    expect(Object.keys(sent).join(' ')).not.toMatch(/version/i)
  })

  it('shows a server refusal and stays on the page', async () => {
    const user = userEvent.setup()
    vi.mocked(api.register).mockRejectedValue({
      response: { status: 422, data: { detail: { error: 'legal_acceptance_required', message: 'You must accept the Terms of Service and the Privacy Policy to continue.' } } },
    })
    render(<RegisterPage />)
    await fill(user)
    await user.click(box())
    await user.click(create())
    expect(await screen.findByRole('alert')).toHaveTextContent('You must accept the Terms of Service')
    expect(router.replace).not.toHaveBeenCalled()
  })

  it('offers the documents from the footer too', () => {
    render(<RegisterPage />)
    const footer = screen.getByRole('navigation', { name: /Terms/ })
    expect(footer.querySelector('a[href="/terms"]')).not.toBeNull()
    expect(footer.querySelector('a[href="/privacy"]')).not.toBeNull()
  })

  it('touch target: the label row is at least 44px tall', () => {
    render(<RegisterPage />)
    expect((box().closest('div')?.querySelector('label') as HTMLElement).className).toContain('min-h-[44px]')
  })

  it('has a visible focus state on the checkbox', () => {
    render(<RegisterPage />)
    expect(box().className).toContain('focus-visible:outline')
  })
})

describe('sign-up is not visually heavy', () => {
  it('adds one line to the form — three fields, one checkbox, one button', () => {
    render(<RegisterPage />)
    expect(screen.getAllByRole('textbox').length + document.querySelectorAll('input[type="password"]').length).toBe(3)
    expect(screen.getAllByRole('checkbox')).toHaveLength(1)
    expect(screen.getAllByRole('button').filter((b) => /Create account/.test(b.textContent ?? ''))).toHaveLength(1)
  })
})

describe('Arabic (RTL)', () => {
  beforeEach(() => useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' }))

  it('reads in Arabic with the links in the right order', () => {
    render(<RegisterPage />)
    const checkbox = screen.getByRole('checkbox', { name: /^أوافق على شروط الخدمة و ?سياسة الخصوصية ?\.$/ })
    expect(checkbox).not.toBeChecked()
    expect(screen.getByRole('link', { name: 'شروط الخدمة' })).toHaveAttribute('href', '/terms')
    expect(screen.getByRole('link', { name: 'سياسة الخصوصية' })).toHaveAttribute('href', '/privacy')
    expect(screen.getByRole('button', { name: /إنشاء حساب/ })).toBeDisabled()
    expect(screen.queryByText('وافق على شروط الخدمة وسياسة الخصوصية لإنشاء حسابك.')).toBeNull()
  })

  it('creates the account once ticked, sending the same agreement', async () => {
    const user = userEvent.setup()
    render(<RegisterPage />)
    await user.type(screen.getByLabelText('الاسم الكامل'), 'أميرة حسن')
    await user.type(screen.getByLabelText('البريد الإلكتروني'), 'amira@example.com')
    await user.type(screen.getByLabelText('كلمة المرور'), 'correcthorsebattery')
    await user.click(screen.getByRole('checkbox'))
    await user.click(screen.getByRole('button', { name: /إنشاء حساب/ }))
    await waitFor(() => expect(api.register).toHaveBeenCalledWith(expect.objectContaining({ accept_terms: true, accept_privacy: true })))
  })
})
