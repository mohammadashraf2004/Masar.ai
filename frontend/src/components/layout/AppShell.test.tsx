import { render, screen, waitFor, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import { AppShell } from '@/components/layout/AppShell'
import { useAuthStore } from '@/lib/store'
import { useLanguageStore } from '@/lib/language'
import { setPathname } from '@/test/nav'
import type { User } from '@/types'

vi.mock('@/lib/api', () => ({ api: { getWallet: vi.fn(), search: vi.fn() } }))
import { api } from '@/lib/api'

const student = (over: Partial<User> = {}): User => ({
  id: 1, email: 'amira@example.com', full_name: 'Amira Hassan', role: 'student', experience_level: 'beginner',
  is_verified: true, overall_readiness_score: 42, created_at: '2026-01-01T00:00:00Z',
  requires_legal_acceptance: false, pending_updates: [], ...over,
})

const signIn = (over: Partial<User> = {}) =>
  useAuthStore.setState({ token: 'tok', expiresAt: null, _hasHydrated: true, user: student(over) })

const renderShell = () => render(<AppShell><p>the page</p></AppShell>)
const sidebar = () => screen.getByRole('complementary')

beforeEach(() => {
  vi.mocked(api.getWallet).mockResolvedValue({ credit_balance: 1240 })
  setPathname('/dashboard')
  signIn()
})

describe('the sidebar', () => {
  it('lists every destination as a link, in the order the navigation defines', () => {
    renderShell()
    const links = within(within(sidebar()).getByRole('navigation', { name: 'Menu' })).getAllByRole('link')
    expect(links.map((a) => a.getAttribute('href'))).toEqual([
      '/', '/dashboard', '/learn', '/learn/my-courses', '/explore', '/tracks', '/tools', '/certificates', '/billing',
      '/glossary', '/mentor', '/community', '/challenges',
    ])
  })

  it('marks the page you are on, and the section when you are inside it', () => {
    setPathname('/tracks/ai-developer')
    renderShell()
    const current = within(sidebar()).getAllByRole('link').filter((a) => a.getAttribute('aria-current') === 'page')
    expect(current.map((a) => a.getAttribute('href'))).toEqual(['/tracks'])
  })

  it('shows the admin page to an admin only', () => {
    const { unmount } = renderShell()
    expect(within(sidebar()).queryByRole('link', { name: 'Admin analytics' })).toBeNull()
    unmount()
    signIn({ role: 'admin' })
    renderShell()
    expect(within(sidebar()).getByRole('link', { name: 'Admin analytics' })).toHaveAttribute('href', '/admin/analytics')
  })

  it('labels the destinations in Arabic for an Arabic reader', () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    renderShell()
    expect(within(sidebar()).getByRole('link', { name: 'تعلّم' })).toHaveAttribute('href', '/learn')
    expect(within(sidebar()).getByRole('link', { name: 'استكشف' })).toHaveAttribute('href', '/explore')
    expect(within(sidebar()).getByRole('link', { name: 'الشهادات' })).toHaveAttribute('href', '/certificates')
  })

  it('leads with the brand, which is one link home named for the product', () => {
    renderShell()
    const brand = within(sidebar()).getAllByRole('link')[0]
    expect(brand).toHaveAttribute('href', '/dashboard')
    // Both scripts are in the DOM (CSS shows one); the second copy is hidden from assistive technology.
    expect(brand).toHaveAccessibleName(/^Masar\s*مسار$/)
    expect(brand.querySelectorAll('[aria-hidden="true"]').length).toBeGreaterThanOrEqual(2)
    expect(brand.querySelector('.brand-en')?.parentElement).toHaveClass('text-[17px]')
    expect(brand.querySelector('.brand-alt-ar')?.parentElement).toHaveClass('text-[17px]')
  })

  it('shows the wallet: the balance, with thousands separated, and the way to top up', async () => {
    renderShell()
    const card = within(sidebar())
    expect(await card.findByText('1,240')).toBeInTheDocument()
    expect(card.getByText('Wallet')).toBeInTheDocument()
    expect(card.getByRole('link', { name: 'Top up credits' })).toHaveAttribute('href', '/billing')
  })

  it('shows a dash rather than a made-up zero until the balance is known', () => {
    vi.mocked(api.getWallet).mockReturnValue(new Promise(() => {}))
    renderShell()
    expect(within(sidebar()).getByText('—')).toBeInTheDocument()
  })

  it('shows who is signed in, with a way to their profile', () => {
    renderShell()
    const row = within(sidebar()).getByRole('link', { name: /Amira Hassan/ })
    expect(row).toHaveAttribute('href', '/profile')
    expect(row).toHaveTextContent('beginner')
  })

  it('does not carry legal links; they live in the page footer', () => {
    renderShell()
    expect(within(sidebar()).queryByRole('link', { name: 'Terms of Use' })).toBeNull()
    expect(within(sidebar()).queryByRole('link', { name: 'Privacy Policy' })).toBeNull()
  })

  // The handoff's sidebar is the brand, the navigation, the wallet and the account. The
  // rest moved: readiness to the dashboard, verification to Certificates.
  it('no longer carries the readiness pill, the quick action or the Get Verified button', () => {
    renderShell()
    const text = sidebar().textContent ?? ''
    expect(text).not.toMatch(/Readiness|Quick action|Ask your AI mentor|Get Verified/)
    expect(within(sidebar()).queryByRole('button')).toBeNull()
  })
})

describe('the header', () => {
  it('has the search, the credit pill, the theme choice and the account menu', async () => {
    renderShell()
    const header = within(screen.getByRole('banner'))
    expect(header.getByRole('combobox', { name: 'Search' })).toBeInTheDocument()
    expect(await header.findByRole('link', { name: '1240 credits' })).toHaveAttribute('href', '/billing')
    expect(header.getByRole('group', { name: 'Theme' })).toBeInTheDocument()
    expect(header.getByRole('button', { name: 'Profile menu: Amira Hassan' })).toBeInTheDocument()
  })

  it('puts the page inside <main>, after the header', () => {
    renderShell()
    const main = screen.getByRole('main')
    expect(main).toHaveTextContent('the page')
    expect(screen.getByRole('banner').compareDocumentPosition(main) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy()
  })

  it('asks for the wallet once, not once per thing that shows it', async () => {
    renderShell()
    await screen.findByRole('link', { name: '1240 credits' })
    expect(api.getWallet).toHaveBeenCalledTimes(1)
  })
})

describe('the mobile menu', () => {
  const openButton = () => screen.getByRole('button', { name: 'Open navigation menu' })

  it('starts closed, and its button says what it controls', () => {
    renderShell()
    expect(openButton()).toHaveAttribute('aria-expanded', 'false')
    expect(openButton()).toHaveAttribute('aria-controls', 'mobile-menu')
    expect(document.getElementById('mobile-menu')).toBeNull()
  })

  it('opens under the header with every destination as a tall row, and the button turns into "close"', async () => {
    const user = userEvent.setup()
    renderShell()
    await user.click(openButton())

    const panel = document.getElementById('mobile-menu') as HTMLElement
    expect(panel).not.toBeNull()
    const rows = within(panel).getAllByRole('link').filter((a) => !['/profile', '/terms', '/privacy'].includes(a.getAttribute('href') ?? ''))
    expect(rows).toHaveLength(13)
    for (const row of rows) expect(row).toHaveClass('min-h-[48px]')
    expect(rows.find((a) => a.getAttribute('aria-current') === 'page')).toHaveAttribute('href', '/dashboard')

    const close = screen.getByRole('button', { name: 'Close navigation menu' })
    expect(close).toHaveAttribute('aria-expanded', 'true')
    expect(close).toHaveAttribute('aria-controls', panel.id)
  })

  it('holds the account, the theme, the language and sign-out in its footer', async () => {
    const user = userEvent.setup()
    renderShell()
    await user.click(openButton())
    const panel = within(document.getElementById('mobile-menu') as HTMLElement)
    expect(panel.getByRole('link', { name: /Amira Hassan/ })).toHaveAttribute('href', '/profile')
    expect(panel.getByRole('group', { name: 'Theme' })).toBeInTheDocument()
    expect(panel.getByRole('button', { name: /EN/ })).toBeInTheDocument() // the language switcher
    expect(panel.getByRole('button', { name: 'Sign out' })).toHaveClass('min-h-[44px]')
    expect(panel.queryByRole('link', { name: 'Terms of Use' })).toBeNull()
    expect(panel.queryByRole('link', { name: 'Privacy Policy' })).toBeNull()
  })

  it('closes when a row is chosen', async () => {
    const user = userEvent.setup()
    document.addEventListener('click', (e) => e.preventDefault(), { once: true, capture: true })
    renderShell()
    await user.click(openButton())
    await user.click(within(document.getElementById('mobile-menu') as HTMLElement).getByRole('link', { name: 'Certificates' }))
    expect(document.getElementById('mobile-menu')).toBeNull()
    expect(openButton()).toHaveAttribute('aria-expanded', 'false')
  })

  it('closes when the dimmed page is tapped', async () => {
    const user = userEvent.setup()
    renderShell()
    await user.click(openButton())
    const scrim = document.querySelector('[class*="bg-scrim"]') as HTMLElement
    expect(scrim).not.toBeNull()
    await user.click(scrim)
    expect(document.getElementById('mobile-menu')).toBeNull()
  })

  it('closes on Escape and hands focus back to its button', async () => {
    const user = userEvent.setup()
    renderShell()
    await user.click(openButton())
    expect(document.getElementById('mobile-menu')).not.toBeNull()
    await user.keyboard('{Escape}')
    expect(document.getElementById('mobile-menu')).toBeNull()
    await waitFor(() => expect(openButton()).toHaveFocus())
  })

  it('stops the page behind it scrolling while it is open, and lets it scroll again after', async () => {
    const user = userEvent.setup()
    renderShell()
    await user.click(openButton())
    expect(document.body.style.overflow).toBe('hidden')
    await user.keyboard('{Escape}')
    expect(document.body.style.overflow).not.toBe('hidden')
  })

  it('is named in Arabic for an Arabic reader', async () => {
    useLanguageStore.setState({ language: 'ar', mode: 'arabic_first' })
    const user = userEvent.setup()
    renderShell()
    await user.click(screen.getByRole('button', { name: 'فتح قائمة التنقل' }))
    expect(screen.getByRole('button', { name: 'إغلاق قائمة التنقل' })).toHaveAttribute('aria-expanded', 'true')
    expect(within(document.getElementById('mobile-menu') as HTMLElement).getByRole('group', { name: 'المظهر' })).toBeInTheDocument()
  })
})

describe('what the walkthroughs point at', () => {
  it('tags the practice and mentor items in the sidebar', () => {
    renderShell()
    const item = (id: string) => within(sidebar()).getByRole('link', { name: id === 'nav-mentor' ? 'AI mentor' : 'Challenges' })
    expect(item('nav-mentor')).toHaveAttribute('data-tour', 'nav-mentor')
    expect(item('nav-practice')).toHaveAttribute('data-tour', 'nav-practice')
    // Nothing else in the rail is a target.
    expect(within(sidebar()).getAllByRole('link').filter((a) => a.hasAttribute('data-tour'))).toHaveLength(2)
  })

  it('has a language switch in the header for the language walkthrough', () => {
    renderShell()
    expect(document.querySelectorAll('header [data-tour="lang-switch"]').length).toBeGreaterThan(0)
  })
})

describe('the walkthrough\'s phone target', () => {
  it('tags the menu button, and the tour never opens the menu itself', () => {
    renderShell()
    const button = screen.getByRole('button', { name: 'Open navigation menu' })
    expect(button).toHaveAttribute('data-tour', 'menu-button')
    expect(button).toHaveAttribute('aria-expanded', 'false')
  })
})
